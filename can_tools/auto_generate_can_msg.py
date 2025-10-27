import cantools
import os
import re
import argparse
import inspect
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Dict, List, Tuple

# ========================= Helpers ========================= #

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

# ========================= Generator ========================= #

def generate_can_msg_py(dbc_path: str, target_id: int, output_dir: str = ".", debug: bool = False):
    db = cantools.database.load_file(dbc_path)
    msg = next((m for m in db.messages if m.frame_id == target_id), None)
    if msg is None:
        raise ValueError(f"❌ 找不到 message ID=0x{target_id:X} 於 {dbc_path}")

    dbc_name = os.path.basename(dbc_path)
    match = re.search(r"(\d{8})", dbc_name)
    version_info = match.group(1) if match else "unknown_version"

    output_file = os.path.join(output_dir, f"generate_0x{target_id:X}.py")

    lines: List[str] = []
    lines.append("# ================================================")
    lines.append("#  Auto-generated CAN Message Encoder/Decoder (with Enums)")
    lines.append(f"#  Source DBC : {dbc_name}")
    lines.append(f"#  DBC Version: {version_info}")
    lines.append(f"#  Generated  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("# ================================================\n")
    # import module 
    lines.append("from typing import Dict, List, Tuple\n")

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
            not_used_keys = []
            for k in sorted(mapping.keys()) :
                if mapping[k] ==  'Not used':
                    not_used_keys.append(k)
                    lines.append(f"    RESERVED_{len(not_used_keys)+1} = {k}")
                else:
                    member = sanitize_enum_member(mapping[k])
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
    lines.append(f"def generate_0x{msg.frame_id:X}_can_msg_bytes(msg: canfd_0x{msg.frame_id:X}_msg, debug: bool = False) -> bytes:")
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
        lines.append(f"                if debug: print(f'Encode {sig.name}: byte[{{byte_i}}] bit {{bit_i}} → {{before:#04x}} → {{after:#04x}}')")
        lines.append("    else:")
        lines.append(f"        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions({sig.name}_OFFSET, {sig.name}_LEN)):")
        lines.append(f"            bit_val = ({lname} >> ({sig.name}_LEN - 1 - i)) & 1")
        lines.append(f"            if bit_val and 0 <= byte_i < len(data):")
        lines.append(f"                before = data[byte_i]")
        lines.append(f"                data[byte_i] |= (1 << bit_i)")
        lines.append(f"                after = data[byte_i]")
        lines.append(f"                if debug: print(f'Encode {sig.name}: byte[{{byte_i}}] bit {{bit_i}} → {{before:#04x}} → {{after:#04x}}')")
    lines.append("    # Materialize to bytes for stable printing/return")
    lines.append("    outb = bytes(data)")
    lines.append("    if debug:")
    lines.append("        print('[DEBUG] Encoded data bytes:', outb.hex(':'))")
    lines.append("    return outb\n")

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
            ctor_args.append(f"{enum_name}({sig.name.lower()})")
        else:
            ctor_args.append(f"{sig.name.lower()}")
    lines.append(f"    return canfd_0x{msg.frame_id:X}_msg({', '.join(ctor_args)})\n")

    # === sample code ===
    lines.append("if __name__ == '__main__':")
    lines.append(f"    msg = canfd_0x{msg.frame_id:X}_msg()")
    lines.append(f"    data = generate_0x{msg.frame_id:X}_can_msg_bytes(msg, debug=True)")
    lines.append(f"    print('Generated CAN FD data:', data.hex(':'))")
    lines.append(f"    decoded = decode_0x{msg.frame_id:X}_can_msg(data, debug=True)")
    lines.append(f"    print('Decoded message:', decoded)")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 已生成 {output_file}")
    print(f"   來源 DBC : {dbc_name}")
    print(f"   Message  : {msg.name} (ID=0x{msg.frame_id:X})")
    print(f"   Signals  : {[sig.name for sig in msg.signals]}")

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
    parser.add_argument("--debug", action="store_true", help="顯示位元層級除錯輸出")
    parser.add_argument("--list", action="store_true", help="列出 DBC 所有 CAN 訊息")
    args = parser.parse_args()

    if args.list:
        list_dbc_messages(args.dbc)
    else:
        if not args.id:
            raise ValueError("請使用 --id 指定要生成的 CAN ID")
        target_id = int(args.id, 16) if str(args.id).startswith("0x") else int(args.id)
        generate_can_msg_py(args.dbc, target_id, args.out, args.debug)
