import cantools
import os
import errno
import json
import re
import argparse
import inspect
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Dict, List, Tuple

# ========================= Helpers ========================= #

def ensure_dir(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        # 路徑已存在但不是資料夾，或路徑非法、沒權限
        raise RuntimeError(f"❌ 無法建立輸出資料夾: {path} ({e})") from e


def unique_member_name(base: str, used: dict) -> str:
    """確保 enum 成員名稱唯一，重複就加 _1, _2 ..."""
    if base not in used:
        used[base] = 0
        return base
    used[base] += 1
    return f"{base}_{used[base]}"

def sanitize_enum_member(name: str) -> str:
    """Sanitize a DBC enum label into SCREAMING_SNAKE_CASE suitable for Python IntEnum members.
    - Replace non-alnum with underscore
    - Collapse multiple underscores
    - Uppercase
    - If starts with a digit or matches a keyword, prefix with '_'
    """
    import keyword
    s = re.sub(r"[^0-9A-Za-z]+", "_", name.strip())
    s = re.sub(r"_+", "_", s).upper()
    if not s:
        s = "VALUE"
    if s[0].isdigit() or keyword.iskeyword(s.lower()):
        s = f"_{s}"
    return s

def get_motorola_bit_positions(start_bit: int, length: int) -> List[Tuple[int, int]]:
    """正確的 Motorola (big_endian) 位元位置對應公式 (byte_index, bit_index)."""
    bits: List[Tuple[int, int]] = []
    for i in range(length):
        bit_position = start_bit - i
        byte_index = bit_position // 8
        bit_index = bit_position % 8
        bits.append((byte_index, bit_index))
    return bits

GEN_FILE_RE = re.compile(r"^generate_0x[0-9A-Fa-f]+\.py$")
def clean_output_dir(out_dir: str) -> None:
    """只刪掉我們產的 generate_0x*.py 跟 generated_index.py"""
    if not os.path.isdir(out_dir):
        return
    for name in os.listdir(out_dir):
        if GEN_FILE_RE.match(name) or name == "generated_index.py":
            os.remove(os.path.join(out_dir, name))
            
def write_generated_index(output_dir: str) -> None:
    """
    掃 output_dir 裡所有 generate_0x*.py，產生 generated_index.py
    內容會是：
        from . import generate_0x117 as can_0x117
        from . import generate_0x210 as can_0x210
        ...
        __all__ = ["can_0x117", "can_0x210", ...]
    """
    pattern = re.compile(r"^generate_0x([0-9A-Fa-f]+)\.py$")
    entries = []
    for fname in sorted(os.listdir(output_dir)):
        m = pattern.match(fname)
        if not m:
            continue
        can_id_hex = m.group(1).upper()  # 讓名稱一致用大寫
        mod_name = f"generate_0x{can_id_hex}"
        alias = f"can_0x{can_id_hex}"
        entries.append((mod_name, alias))

    if not entries:
        return  # 沒有檔就不寫

    lines = []
    for mod_name, alias in entries:
        lines.append(f"from . import {mod_name} as {alias}")
    all_names = ", ".join(f'"{alias}"' for _, alias in entries)
    lines.append("")
    lines.append(f"__all__ = [{all_names}]")
    lines.append("")

    index_path = os.path.join(output_dir, "generated_index.py")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ========================= Generator ========================= #

def generate_can_msg_py(dbc_path: str, target_id: int, output_dir: str = ".", debug: bool = False, strict: bool = False, filename_prefix: str = ""):
    db = cantools.database.load_file(dbc_path)
    msg = next((m for m in db.messages if m.frame_id == target_id), None)
    if msg is None:
        raise ValueError(f"❌ 找不到 message ID=0x{target_id:X} 於 {dbc_path}")

    dbc_name = os.path.basename(dbc_path)
    match = re.search(r"(\d{8})", dbc_name)
    version_info = match.group(1) if match else "unknown_version"
    
    output_file = os.path.join(output_dir, f"{filename_prefix}generate_0x{target_id:X}.py")

    lines: List[str] = []
    lines.append("# ================================================")
    lines.append("#  Auto-generated CAN Message Encoder/Decoder (with Enums)")
    lines.append(f"#  Source DBC : {dbc_name}")
    lines.append(f"#  DBC Version: {version_info}")
    lines.append(f"#  Generated  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("# ================================================\n")
    # import module 
    lines.append("from typing import Dict, List, Tuple")
    lines.append("import re")
    lines.append("")
    
    # === Enum strict/loose switch (emitted into generated file) ===
    lines.append(f"STRICT_ENUM = {'True' if strict else 'False'}  # loose by default; set True to raise on unknown enum values")
    lines.append("def to_enum(cls, value, strict: bool = False):")
    lines.append("    \"\"\"Cast integer to IntEnum; if strict=False and value is unknown, return the raw int.\"\"\"")
    lines.append("    try:")
    lines.append("        return cls(int(value))")
    lines.append("    except Exception:")
    lines.append("        if strict:")
    lines.append("            raise")
    lines.append("        return int(value)")
    lines.append("")

    # emit helpers we depend on
    lines.append(inspect.getsource(sanitize_enum_member))
    lines.append(inspect.getsource(get_motorola_bit_positions))
    # ===== Collect and emit ENUMS from value descriptions =====
    # Build a mapping: signal_name -> {value:int : label:str}
    signal_enums: Dict[str, Dict[int, str]] = {}
    for sig in msg.signals:
        # cantools uses .choices; some versions expose .value_descriptions
        choices = getattr(sig, "choices", None) or getattr(sig, "value_descriptions", None)
        if choices:
            # Ensure int keys
            normalized: Dict[int, str] = {int(k): str(v) for k, v in dict(choices).items()}
            signal_enums[sig.name] = normalized

    if signal_enums:
        lines.append("from enum import IntEnum\n")
        for sig_name, mapping in signal_enums.items():
            enum_name = f"{sig_name}Enum"
            lines.append(f"class {enum_name}(IntEnum):")
            # Preserve key order (sorted by numeric value)
            used_members = {}  # 用來記錄已經出現過的名稱
            for k in sorted(mapping.keys()) :
                raw_val = mapping[k].strip() if mapping[k] is not None else "UNKNOWN"
                member = sanitize_enum_member(raw_val)  # 先轉成合法 Python 名稱
                member = unique_member_name(member, used_members)
                lines.append(f"    {member} = {k}")
            lines.append("")

    # ===== Constants for bit layout =====
    lines.append(f"# Message: {msg.name} (ID=0x{msg.frame_id:X}, DLC={msg.length})\n")
    for sig in msg.signals:
        lines.append(f"{sig.name}_OFFSET = {sig.start}")
        lines.append(f"{sig.name}_LEN = {sig.length}")
        lines.append(f"{sig.name}_BYTE_ORDER = '{sig.byte_order}'")
    lines.append("")

    # ===== Dataclass for message =====
    lines.append("from dataclasses import dataclass\n")
    lines.append(f"@dataclass\nclass canfd_0x{msg.frame_id:X}_msg:")
    for sig in msg.signals:
        if sig.name in signal_enums:
            enum_name = f"{sig.name}Enum"
            # Default = smallest key
            default_key = sorted(signal_enums[sig.name].keys())[0]
            default_member = sanitize_enum_member(signal_enums[sig.name][default_key])
            lines.append(f"    {sig.name}: {enum_name} = {enum_name}.{default_member}")
        else:
            lines.append(f"    {sig.name}: int = 0")
    lines.append("")

    # ===== Encode function =====
    lines.append(f"def generate_0x{msg.frame_id:X}_can_msg_bytes(msg: canfd_0x{msg.frame_id:X}_msg, debug: bool = False) -> List[int]:")
    lines.append("    data = bytearray(64)")
    for sig in msg.signals:
        lname = sig.name.lower()
        if sig.name in signal_enums:
            # cast enum to int when using
            lines.append(f"    {lname} = int(msg.{sig.name})")
        else:
            lines.append(f"    {lname} = msg.{sig.name}")
        lines.append(f"    if {sig.name}_BYTE_ORDER == 'little_endian':")
        lines.append(f"        for i in range({sig.name}_LEN):")
        lines.append(f"            bit_pos = {sig.name}_OFFSET + i")
        lines.append(f"            byte_i = bit_pos // 8")
        lines.append(f"            bit_i = bit_pos % 8")
        lines.append(f"            if ({lname} >> i) & 1:")
        lines.append(f"                before = data[byte_i]")
        lines.append(f"                data[byte_i] |= (1 << bit_i)")
        lines.append(f"                after = data[byte_i]")
        lines.append(f"                if debug: print(f'Encode {sig.name}: byte{{byte_i}} bit {{bit_i}} → {{before:#04x}} → {{after:#04x}}')")
        lines.append("    else:")
        lines.append(f"        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions({sig.name}_OFFSET, {sig.name}_LEN)):")
        lines.append(f"            bit_val = ({lname} >> ({sig.name}_LEN - 1 - i)) & 1")
        lines.append(f"            if bit_val and 0 <= byte_i < len(data):")
        lines.append(f"                before = data[byte_i]")
        lines.append(f"                data[byte_i] |= (1 << bit_i)")
        lines.append(f"                after = data[byte_i]")
        lines.append(f"                if debug: print(f'Encode {sig.name}: byte{{byte_i}} bit {{bit_i}} → {{before:#04x}} → {{after:#04x}}')")
    lines.append("    # Materialize to bytes for stable printing/return")
    lines.append("    outb = bytes(data)")
    lines.append("    if debug:")
    lines.append("        print('[DEBUG] Encoded data bytes:', outb.hex(':'))")
    lines.append("        print('[DEBUG] Encoded data list:', list(outb))")
    lines.append("    return list(outb)\n")

    # ===== Decode function =====
    lines.append(f"def decode_0x{msg.frame_id:X}_can_msg(data: bytes, debug: bool = False) -> canfd_0x{msg.frame_id:X}_msg:")
    for sig in msg.signals:
        lines.append(f"    {sig.name.lower()} = 0")
    lines.append("")
    for sig in msg.signals:
        lname = sig.name.lower()
        lines.append(f"    if {sig.name}_BYTE_ORDER == 'little_endian':")
        lines.append(f"        for i in range({sig.name}_LEN):")
        lines.append(f"            bit_pos = {sig.name}_OFFSET + i")
        lines.append(f"            byte_i = bit_pos // 8")
        lines.append(f"            bit_i = bit_pos % 8")
        lines.append(f"            if (data[byte_i] >> bit_i) & 1:")
        lines.append(f"                {lname} |= (1 << i)")
        lines.append(f"                if debug: print(f'Decode {sig.name}: byte={{byte_i}}, bit={{bit_i}}, val=1')")
        lines.append("    else:")
        lines.append(f"        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions({sig.name}_OFFSET, {sig.name}_LEN)):")
        lines.append(f"            if (data[byte_i] >> bit_i) & 1:")
        lines.append(f"                {lname} |= (1 << ({sig.name}_LEN - 1 - i))")
        lines.append(f"                if debug: print(f'Decode {sig.name}: byte={{byte_i}}, bit={{bit_i}}, val=1')")
        lines.append("")
    # Construct dataclass with proper Enum if available
    ctor_args: List[str] = []
    for sig in msg.signals:
        if sig.name in signal_enums:
            enum_name = f"{sig.name}Enum"
            # STRICT_ENUM hook
            ctor_args.append(f"to_enum({enum_name}, {sig.name.lower()}, STRICT_ENUM)")
        else:
            ctor_args.append(f"{sig.name.lower()}")
    lines.append(f"    return canfd_0x{msg.frame_id:X}_msg({', '.join(ctor_args)})\n")

    # === sample code ===
    lines.append("if __name__ == '__main__':")
    # Pretty, explicit constructor with all fields shown for copy-paste friendliness
    lines.append(f"    msg = canfd_0x{msg.frame_id:X}_msg(")
    for i, sig in enumerate(msg.signals):
        if sig.name in signal_enums:
            default_key = sorted(signal_enums[sig.name].keys())[0]
            default_member = sanitize_enum_member(signal_enums[sig.name][default_key])
            lines.append(f"        {sig.name}={sig.name}Enum.{default_member},  # default: {sig.name}Enum.{default_member}({default_key})")
        else:
            lines.append(f"        {sig.name}=0,  # default: 0")
    lines.append("    )")
    # Generate list[int], also print hex for easy inspection
    lines.append(f"    data_list = generate_0x{msg.frame_id:X}_can_msg_bytes(msg)")
    lines.append("    print('Generated CAN FD data (list):', data_list)")
    lines.append("    data_bytes = bytes(data_list)")
    lines.append("    print('Generated CAN FD data (hex):', data_bytes.hex(':'))")
    lines.append(f"    decoded = decode_0x{msg.frame_id:X}_can_msg(data_bytes)")
    lines.append("    print('Decoded message:', decoded)")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 已生成 {output_file}")
    print(f"   來源 DBC : {dbc_name}")
    print(f"   Message  : {msg.name} (ID=0x{msg.frame_id:X})")
    print(f"   Signals  : {[sig.name for sig in msg.signals]}")


# ---------------------------------------------------------
# 產出 OPC UA 節點 json (snake_case)
# ---------------------------------------------------------
def generate_opcua_json_from_dbc(can_messages, output_path: str, namespace_index: int = 2, bus_name: str = "can0"):
    """
    產出格式大致如下：

    {
      "can_buses": [...],
      "messages": [
         {
            "name": "instrument_cluster_status",
            "can_id": "0x117",
            "bus": "can0",
            "dlc": 8,
            "signals": [
               {
                 "name": "vehicle_speed",
                 "start_bit": 16,
                 "bit_length": 16,
                 "byte_order": "intel",
                 "value_type": "uint",
                 "scale": 0.1,
                 "offset": 0.0,
                 "opcua": {
                   "node_id": "ns=2;s=can/instrument_cluster_status/vehicle_speed",
                   "browse_name": "vehicle_speed",
                   "data_type": "Float",
                   "access_level": "current_read"
                 }
               }
            ]
         }
      ]
    }
    """
    result = {
        "can_buses": [
            {
                "name": bus_name,
                # bitrate 寫不出來就先不寫，也可以讓使用者之後補
            }
        ],
        "messages": []
    }

    for msg in can_messages:
        msg_entry = {
            "name": msg.name.lower(),
            "can_id": f"0x{msg.frame_id:X}",
            "bus": bus_name,
            "dlc": msg.length,
            "signals": []
        }

        for sig in msg.signals:
            # 判斷大小端
            byte_order = "motorola" if sig.byte_order == "big_endian" else "intel"

            # 預設都當成讀取節點
            opcua_block = {
                "node_id": f"ns={namespace_index};s=can/{msg.name}/{sig.name}",
                "browse_name": sig.name.lower(),
                # 根據型別稍微判斷一下
                "data_type": "Float" if sig.is_float else "UInt32",
                "access_level": "current_read"
            }

            # 如果 DBC 有 choices，就當 enum，看起來比較像 discrete
            if sig.choices:
                opcua_block["enum_map"] = {str(k): str(v) for k, v in sig.choices.items()}
                # CAN 常見的 enum 都不大，用 UInt16 就夠
                opcua_block["data_type"] = "UInt16"

            signal_entry = {
                "name": sig.name.lower(),
                "start_bit": sig.start,
                "bit_length": sig.length,
                "byte_order": byte_order,
                "value_type": "float" if sig.is_float else "uint",
                "scale": sig.scale,
                "offset": sig.offset,
                "opcua": opcua_block
            }

            msg_entry["signals"].append(signal_entry)

        result["messages"].append(msg_entry)

    # 寫檔
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[opcua gen] saved to {output_path}")

# ---------------------------------------------------------
# 產出 open62541 節點 json (snake_case)
# ---------------------------------------------------------
def generate_opcua_json_open62541(can_messages,
                                  output_path: str,
                                  namespace_index: int = 2,
                                  namespace_uri: str = "urn:can-opcua-demo"):
    """
    產生一份比較好給 open62541 消費的 JSON：
    {
      "namespace_uri": "...",
      "namespace_index": 2,
      "nodes": [
         { ... object ... },
         { ... variable ... }
      ]
    }
    每一個 CAN ID 變成一個 Object，底下的 signal 變成 Variable。
    """
    nodes = []

    # 先放一個 CAN 的根節點
    can_root_nodeid = f"ns={namespace_index};s=can"
    nodes.append({
        "node_id": can_root_nodeid,
        "browse_name": f"{namespace_index}:can",
        "display_name": "CAN",
        "parent": "ns=0;i=85",          # ObjectsFolder
        "parent_ref": "Organizes",
        "node_class": "Object"
    })

    for msg in can_messages:
        # 每個 CAN message 先掛一個 Object
        msg_nodeid = f"ns={namespace_index};s=can/0x{msg.frame_id:X}"
        nodes.append({
            "node_id": msg_nodeid,
            "browse_name": f"{namespace_index}:0x{msg.frame_id:X}",
            "display_name": msg.name,
            "parent": can_root_nodeid,
            "parent_ref": "Organizes",
            "node_class": "Object"
        })

        for sig in msg.signals:
            # 型別粗略推一下
            if sig.is_float:
                ua_type = "Float"
            else:
                if sig.length <= 8:
                    ua_type = "Byte"
                elif sig.length <= 16:
                    ua_type = "UInt16"
                elif sig.length <= 32:
                    ua_type = "UInt32"
                else:
                    ua_type = "UInt64"

            var_nodeid = f"ns={namespace_index};s=can/0x{msg.frame_id:X}/{sig.name}"
            nodes.append({
                "node_id": var_nodeid,
                "browse_name": f"{namespace_index}:{sig.name}",
                "display_name": sig.name,
                "parent": msg_nodeid,
                "parent_ref": "Organizes",
                "node_class": "Variable",
                "data_type": ua_type,
                "value_rank": -1,
                "access_level": 1,   # 1=read, 要寫就改 3
                # 把 CAN 用的資訊塞在這裡，open62541 實作時可以拿來解 bit
                "can_meta": {
                    "can_id": f"0x{msg.frame_id:X}",
                    "start_bit": sig.start,
                    "bit_length": sig.length,
                    "byte_order": "motorola" if sig.byte_order == "big_endian" else "intel",
                    "scale": sig.scale,
                    "offset": sig.offset
                }
            })

    data = {
        "namespace_uri": namespace_uri,
        "namespace_index": namespace_index,
        "nodes": nodes
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[opcua-open62541] saved to {output_path}")


def list_dbc_messages(dbc_path: str):
    db = cantools.database.load_file(dbc_path)
    for msg in db.messages:
        print(f"Message: {msg.name}, ID: {hex(msg.frame_id)}, DLC: {msg.length}")
        for sig in msg.signals:
            if sig.byte_order == "big_endian":
                end_bit = sig.start - sig.length + 1
            else:
                end_bit = sig.start + sig.length - 1
            print(f"   Signal: {sig.name} ({sig.start}..{end_bit} bits) order: {sig.byte_order}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自動從 DBC 生成 CAN encode/decode 程式 (Hybrid + Debug + List)")
    parser.add_argument("--dbc", required=True, help="指定 DBC 檔案路徑")
    parser.add_argument("--id", help="指定目標 CAN ID (例如 0x495 或 1173)")
    parser.add_argument("--out", default=".", help="輸出目錄 (預設目前目錄)")
    parser.add_argument("--prefix", default="", help="(可選) 產生檔名前綴，例如 'IVI_' → 產出 IVI_generate_0x*.py")
    parser.add_argument("--debug", action="store_true", help="顯示位元層級除錯輸出")
    parser.add_argument("--list", action="store_true", help="列出 DBC 所有 CAN 訊息")
    parser.add_argument("--strict", action="store_true", help="Enum 嚴格模式：遇到未定義的枚舉值即拋出錯誤（預設為寬鬆模式）")
    parser.add_argument("--clean-out", action="store_true", help="產生前先清掉 out 目錄裡舊的 auto-generated 檔案")
    
    # 輸出 OPC UA json
    parser.add_argument("--opcua-json", help="output json file for opcua nodes")
    parser.add_argument("--opcua-ns", type=int, default=2, help="opc ua namespace index (default=2)")
    parser.add_argument("--bus-name", default="can0", help="bus name to put in json (default=can0)")
    parser.add_argument("--opcua-json-open62541", help="output open62541-friendly opcua nodes json file")
    parser.add_argument("--opcua-ns-uri", default="urn:can-opcua-demo", help="namespace uri for open62541 json")

    args = parser.parse_args()

    if args.list:
        list_dbc_messages(args.dbc)
    else:
        # Ensure the output folder exists.
        out_dir = args.out or "."   # 空字串也當成 "."
        if out_dir != ".":
            ensure_dir(out_dir)
            
        if args.clean_out:
            clean_output_dir(out_dir)
        
        if not args.id:
            raise ValueError("請使用 --id 指定要生成的 CAN ID；或使用 --id all 生成全部")
        
        if not os.path.exists(args.dbc):
            raise ValueError(f"指定DBC({args.dbc})不存在")

        db = cantools.database.load_file(args.dbc)        
        if str(args.id).lower() == 'all':
            for m in db.messages:
                generate_can_msg_py(args.dbc, m.frame_id, args.out, args.debug, strict=args.strict, filename_prefix=args.prefix)
        else:
            target_id = int(args.id, 16) if str(args.id).startswith("0x") else int(args.id)
            generate_can_msg_py(args.dbc, target_id, args.out, args.debug, strict=args.strict, filename_prefix=args.prefix)
            
        write_generated_index(out_dir)
        
        # Python can-opcua server版輸出
        if args.opcua_json:
            if str(args.id).lower() == 'all':
                generate_opcua_json_from_dbc(db.messages, args.opcua_json, args.opcua_ns, args.bus_name)
            else:
                target_messages = [msg for msg in db.messages if msg.frame_id == target_id]
                generate_opcua_json_from_dbc(target_messages, args.opcua_json, args.opcua_ns, args.bus_name)
        
        # open62541 版的輸出
        if args.opcua_json_open62541:
            if str(args.id).lower() == 'all':
                generate_opcua_json_open62541(
                    db.messages,
                    args.opcua_json_open62541,
                    namespace_index=args.opcua_ns,
                    namespace_uri=args.opcua_ns_uri
                )
            else:
                target_messages = [msg for msg in db.messages if msg.frame_id == target_id]
                generate_opcua_json_open62541(
                    target_messages,
                    args.opcua_json_open62541,
                    namespace_index=args.opcua_ns,
                    namespace_uri=args.opcua_ns_uri
                )
