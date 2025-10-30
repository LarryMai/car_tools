#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, importlib, logging, threading, time, queue, signal, sys, os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if hasattr(os, "add_dll_directory"):
    try: os.add_dll_directory(str(SCRIPT_DIR))
    except Exception: pass
    kd = SCRIPT_DIR / "kerneldlls"
    if kd.exists():
        try: os.add_dll_directory(str(kd))
        except Exception: pass

def _ensure_zlg_loaded():
    import importlib
    return importlib.import_module("zlgcan")

class CanParserAdapter:
    def __init__(self, module_name: str):
        mod = importlib.import_module(module_name)
        self._parse = getattr(mod, "parse_frame", None)
        self._encode = getattr(mod, "encode_signals", None)
        if self._parse is None:
            raise RuntimeError(f"{module_name} must define parse_frame(can_id:int,data:bytes)->dict")
        if self._encode is None:
            logging.warning("encode_signals() not found; only parse/respond(raw) will work.")
    def parse(self, can_id: int, data: bytes) -> Dict[str, Any]:
        return self._parse(can_id, data)
    def encode(self, updates: Dict[str, Any]) -> List[Tuple[int, bytes]]:
        if self._encode is None: return []
        return list(self._encode(updates))

DEFAULT_CONFIG_YAML = r"""
periodic:
  - name: VehicleStateTick
    interval_ms: 100
    signals:
      MeterIndSpeed_raw32: 1200
      FD_EDrive_System: 1
    formulas:
      FDC_VCU_LVChrgFreq_Sta: "(state.get('FDC_VCU_LVChrgFreq_Sta', 0) + 1) % 3"
respond:
  - name: PingPong117
    request_id: 0x117
    response:
      signals:
        FD_Telltale_Fail: "(state.get('FD_Telltale_Fail', 0) ^ 1)"
startup_burst:
  - name: Hello117
    delay_ms: 0
    signals:
      PwrSta: 4
      ShiftGearPosn: 5
"""
try:
    import yaml
except Exception:
    yaml = None

@dataclass
class PeriodicJob:
    name: str
    interval_ms: int
    signals: Dict[str, Any] = field(default_factory=dict)
    formulas: Dict[str, str] = field(default_factory=dict)
@dataclass
class ResponseRule:
    name: str
    request_id: int
    request_mask: Optional[bytes] = None
    request_data: Optional[bytes] = None
    resp_signals: Dict[str, Any] = field(default_factory=dict)
    raw_can_id: Optional[int] = None
    raw_data: Optional[bytes] = None
@dataclass
class StartupBurst:
    name: str
    delay_ms: int
    signals: Dict[str, Any] = field(default_factory=dict)
@dataclass
class SimConfig:
    periodic: List[PeriodicJob] = field(default_factory=list)
    respond: List[ResponseRule] = field(default_factory=list)
    startup_burst: List[StartupBurst] = field(default_factory=list)

def _hx(s: Optional[str]) -> Optional[bytes]:
    if s is None: return None
    s = s.strip().replace(" ","")
    return bytes.fromhex(s)

def load_config(path: Optional[str]) -> SimConfig:
    cfg_text = DEFAULT_CONFIG_YAML
    if path:
        if yaml is None:
            raise RuntimeError("PyYAML not installed; cannot load external config. pip install pyyaml")
        with open(path, "r", encoding="utf-8") as f:
            cfg_text = f.read()
    data = yaml.safe_load(cfg_text) if yaml else {}
    periodic, respond, startup_burst = [], [], []
    for p in (data.get("periodic") or []):
        periodic.append(PeriodicJob(
            name=str(p.get("name","job")),
            interval_ms=int(p.get("interval_ms",100)),
            signals=dict(p.get("signals") or {}),
            formulas=dict(p.get("formulas") or {}),
        ))
    for r in (data.get("respond") or []):
        resp = r.get("response") or {}
        respond.append(ResponseRule(
            name=str(r.get("name","rule")),
            request_id=int(str(r.get("request_id")),0),
            request_mask=_hx(r.get("request_mask")),
            request_data=_hx(r.get("request_data")),
            resp_signals=dict(resp.get("signals") or {}),
            raw_can_id=(int(str(resp.get("can_id")),0) if resp.get("can_id") is not None else None),
            raw_data=_hx(resp.get("data")),
        ))
    for b in (data.get("startup_burst") or []):
        startup_burst.append(StartupBurst(
            name=str(b.get("name","burst")),
            delay_ms=int(b.get("delay_ms",0)),
            signals=dict(b.get("signals") or {}),
        ))
    return SimConfig(periodic=periodic, respond=respond, startup_burst=startup_burst)

def _eval_formula(expr: str, state: Dict[str, Any], tnow_ms: float) -> Any:
    return eval(expr, {"__builtins__": {}}, {"state": state, "tnow_ms": tnow_ms})

def _build_dev_map(zcanlib) -> Dict[str, int]:
    names = [
        "ZCAN_USBCANFD_100U",
        "ZCAN_USBCANFD_100U_MINI",
        "ZCAN_USBCANFD_200U",
        "ZCAN_USBCANFD_400U",
        "ZCAN_USBCANFD_800U",
    ]
    dev_map = {}
    for nm in names:
        val = getattr(zcanlib, nm, None)
        if val is not None:
            dev_map[nm.replace("ZCAN_", "")] = val
    return dev_map

def zlg_open_device(zcanlib, dev_type: str, dev_idx: int) -> int:
    dev_map = _build_dev_map(zcanlib)
    dtype = dev_map.get(dev_type.upper())
    if dtype is None:
        raise RuntimeError(f"Unsupported dev type '{dev_type}'. Choose one of: {list(dev_map.keys())}")
    lib = zcanlib.ZCAN()
    handle = lib.OpenDevice(dtype, dev_idx, 0)
    if handle == getattr(zcanlib, "INVALID_DEVICE_HANDLE", 0):
        raise RuntimeError("OpenDevice failed")
    return handle

def zlg_start_channel(zcanlib, dev_handle: int, chn: int, abit: int, dbit: int, loopback: bool=False) -> int:
    lib = zcanlib.ZCAN()
    if lib.ZCAN_SetValue(dev_handle, f"{chn}/canfd_abit_baud_rate", str(abit).encode("utf-8")) != getattr(zcanlib, "ZCAN_STATUS_OK", 1):
        raise RuntimeError("Set arbitration bitrate failed")
    if lib.ZCAN_SetValue(dev_handle, f"{chn}/canfd_dbit_baud_rate", str(dbit).encode("utf-8")) != getattr(zcanlib, "ZCAN_STATUS_OK", 1):
        raise RuntimeError("Set data bitrate failed")
    lib.ZCAN_SetValue(dev_handle, f"{chn}/initenal_resistance", b"1")
    cfg = zcanlib.ZCAN_CHANNEL_INIT_CONFIG()
    cfg.can_type = getattr(zcanlib, "ZCAN_TYPE_CANFD", 1)
    cfg.config.canfd.mode = 1 if loopback else 0
    chn_handle = lib.InitCAN(dev_handle, chn, cfg)
    if chn_handle is None:
        raise RuntimeError("InitCAN failed")
    lib.ZCAN_SetValue(dev_handle, f"{chn}/set_device_tx_echo", b"0")
    if lib.StartCAN(chn_handle) != getattr(zcanlib, "ZCAN_STATUS_OK", 1):
        raise RuntimeError("StartCAN failed")
    return chn_handle

class ZlgSimServer:
    def __init__(self, zcanlib, dev_handle: Optional[int], chn_handle: Optional[int],
                 parsers_by_id: Dict[Optional[int], CanParserAdapter], cfg: SimConfig, dry_run: bool=False):
        self.zcanlib, self.dev_handle, self.chn_handle = zcanlib, dev_handle, chn_handle
        self.parsers_by_id = parsers_by_id
        self.cfg, self.dry_run = cfg, dry_run
        self.state: Dict[str, Any] = {}
        self._stop = threading.Event()
        self._tx_q: "queue.Queue[Tuple[int, bytes]]" = queue.Queue()
        self._threads: List[threading.Thread] = []

    def _choose_parser(self, can_id:int) -> Optional[CanParserAdapter]:
        return self.parsers_by_id.get(can_id) or self.parsers_by_id.get(None)

    def start(self) -> None:
        if self.chn_handle is not None:
            t = threading.Thread(target=self._rx_loop, name="rx", daemon=True)
            t.start(); self._threads.append(t)
        ttx = threading.Thread(target=self._tx_loop, name="tx", daemon=True)
        ttx.start(); self._threads.append(ttx)
        for b in self.cfg.startup_burst:
            threading.Timer(b.delay_ms/1000.0, self._enqueue_signals, args=(b.signals, f"startup:{b.name}")).start()
        for job in self.cfg.periodic:
            t = threading.Thread(target=self._periodic_loop, args=(job,), name=f"per:{job.name}", daemon=True)
            t.start(); self._threads.append(t)

    def stop(self) -> None:
        self._stop.set()
        for t in self._threads: t.join(timeout=0.5)

    def _rx_loop(self) -> None:
        assert self.chn_handle is not None
        lib = self.zcanlib.ZCAN()
        logging.info("RX loop started")
        while not self._stop.is_set():
            rcv_canfd_num = lib.GetReceiveNum(self.chn_handle, getattr(self.zcanlib, "ZCAN_TYPE_CANFD", 1))
            if rcv_canfd_num:
                n = min(rcv_canfd_num, 200)
                msgs, got = lib.ReceiveFD(self.chn_handle, n, 100)
                for i in range(got):
                    frame = msgs[i].frame
                    can_id = frame.can_id & 0x1FFFFFFF
                    data = bytes(frame.data[:frame.len])
                    parser = self._choose_parser(can_id)
                    if parser:
                        try:
                            dec = parser.parse(can_id, data)
                            if dec: self.state.update(dec)
                        except Exception:
                            logging.exception("Decode FD error 0x%X", can_id)
                    try:
                        self._maybe_respond(can_id, data)
                    except Exception:
                        logging.exception("Respond FD error 0x%X", can_id)
            rcv_num = lib.GetReceiveNum(self.chn_handle, getattr(self.zcanlib, "ZCAN_TYPE_CAN", 0))
            if rcv_num:
                n = min(rcv_num, 200)
                msgs, got = lib.Receive(self.chn_handle, n, 100)
                for i in range(got):
                    frame = msgs[i].frame
                    can_id = frame.can_id & 0x1FFFFFFF
                    if frame.can_id & (1<<30): data = b""
                    else:
                        dlc = frame.can_dlc
                        data = bytes(frame.data[:dlc])
                    parser = self._choose_parser(can_id)
                    if parser:
                        try:
                            dec = parser.parse(can_id, data)
                            if dec: self.state.update(dec)
                        except Exception:
                            logging.exception("Decode error 0x%X", can_id)
                    try:
                        self._maybe_respond(can_id, data)
                    except Exception:
                        logging.exception("Respond error 0x%X", can_id)
            time.sleep(0.001)

    def _tx_loop(self) -> None:
        logging.info("TX loop started (dry_run=%s)", self.dry_run)
        while not self._stop.is_set():
            try:
                can_id, payload = self._tx_q.get(timeout=0.1)
            except queue.Empty:
                continue
            if self.dry_run or self.chn_handle is None:
                print(f"TX 0x{can_id:X} {payload.hex()}"); continue
            try:
                lib = self.zcanlib.ZCAN()
                if len(payload) > 8:
                    obj = self.zcanlib.ZCAN_TransmitFD_Data()
                    obj.transmit_type = 0
                    obj.frame.can_id = can_id | (1<<31 if can_id>0x7FF else 0)
                    obj.frame.len = len(payload)
                    obj.frame.flags |= 0x1  # BRS
                    for i,b in enumerate(payload): obj.frame.data[i]=b
                    lib.TransmitFD(self.chn_handle, (self.zcanlib.ZCAN_TransmitFD_Data*1)(obj), 1)
                else:
                    obj = self.zcanlib.ZCAN_Transmit_Data()
                    obj.transmit_type = 0
                    obj.frame.can_id = can_id | (1<<31 if can_id>0x7FF else 0)
                    obj.frame.can_dlc = len(payload)
                    for i,b in enumerate(payload): obj.frame.data[i]=b
                    lib.Transmit(self.chn_handle, (self.zcanlib.ZCAN_Transmit_Data*1)(obj), 1)
            except Exception as e:
                logging.error("ZLG send error 0x%X: %s", can_id, e)

    def _enqueue_signals(self, signals: Dict[str, Any], tag: str="") -> None:
        tnow_ms = time.time()*1000.0
        prepared: Dict[str, Any] = {}
        for k,v in signals.items():
            prepared[k] = _eval_formula(v, self.state, tnow_ms) if isinstance(v, str) else v
        parser = self.parsers_by_id.get(None)
        targets = []
        if parser:
            targets.append(parser)
        else:
            targets.extend(self.parsers_by_id.values())
        for pr in targets:
            frames = pr.encode(dict(prepared))
            for can_id, payload in frames:
                self._tx_q.put((can_id, payload))

    def _periodic_loop(self, job: PeriodicJob) -> None:
        next_ts = time.time()
        while not self._stop.is_set():
            now = time.time()
            if now >= next_ts:
                signals = dict(job.signals)
                if job.formulas:
                    tnow_ms = now*1000.0
                    for k, expr in job.formulas.items():
                        signals[k] = _eval_formula(expr, self.state, tnow_ms)
                self._enqueue_signals(signals, tag=f"periodic:{job.name}")
                next_ts = now + job.interval_ms/1000.0
            time.sleep(0.001)

    def _maybe_respond(self, can_id: int, data: bytes) -> None:
        for rule in self.cfg.respond:
            if can_id != rule.request_id: continue

            if rule.request_mask is not None and rule.request_data is not None:
            # 使用 bytes(8) 取代 b"\x00"*8，避免某些編輯器把 escape 字面量注入實體 NUL
                mask = (rule.request_mask + bytes(8))[:8]
                rdat = (rule.request_data + bytes(8))[:8]
                if bytes(d & m for d, m in zip(data, mask)) != bytes(r & m for r, m in zip(rdat, mask)):
                    continue
            if rule.resp_signals:
                self._enqueue_signals(rule.resp_signals, tag=f"resp:{rule.name}")
            elif rule.raw_can_id is not None and rule.raw_data is not None:
                self._tx_q.put((rule.raw_can_id, rule.raw_data))

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ZLG USBCANFD-based Simulate/Response Server (multi-adapter, local DLLs only)")
    p.add_argument("--parser-mod", help="Single adapter module path (e.g., dbc_adapters.generator_adapter_0x117)")
    p.add_argument("--dbc-adapter-dir", help="Adapter package folder (e.g., dbc_adapters). Used with --id-list.")
    p.add_argument("--id-list", help="Comma-separated CAN IDs, e.g., '0x117,0x210'. Used with --dbc-adapter-dir.")
    p.add_argument("--config", help="YAML config path")
    p.add_argument("--dev-type", default="USBCANFD_100U", help="Device key, e.g., USBCANFD_100U|USBCANFD_200U|...")
    p.add_argument("--dev-idx", type=int, default=0)
    p.add_argument("--chan", type=int, default=0)
    p.add_argument("--abit", type=int, default=500000)
    p.add_argument("--dbit", type=int, default=2000000)
    p.add_argument("--loopback", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--log-level", default="INFO", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    return p.parse_args()

def _load_parsers_from_ids(dir_name:str, id_list:str) -> Dict[Optional[int], CanParserAdapter]:
    result : Dict[Optional[int], CanParserAdapter] = {}
    ids = [int(s.strip(),0) for s in id_list.split(",") if s.strip()]
    for cid in ids:
        modname = f"{dir_name}.generator_adapter_0x{cid:03X}"
        result[cid] = CanParserAdapter(modname)
        logging.info("Loaded adapter: %s (ID=0x%X)", modname, cid)
    return result

def main() -> int:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="[%(levelname)s] %(message)s")
    cfg = load_config(args.config)

    parsers_by_id : Dict[Optional[int], CanParserAdapter] = {}
    if args.parser_mod:
        parsers_by_id[None] = CanParserAdapter(args.parser_mod)
        logging.info("Single adapter: %s", args.parser_mod)
    elif args.dbc_adapter_dir and args.id_list:
        parsers_by_id = _load_parsers_from_ids(args.dbc_adapter_dir, args.id_list)
    else:
        raise SystemExit("Provide --parser-mod OR (--dbc-adapter-dir AND --id-list).")

    zcanlib = None
    dev_handle = chn_handle = None
    if not args.dry_run:
        zcanlib = _ensure_zlg_loaded()
        dev_handle = zlg_open_device(zcanlib, args.dev_type, args.dev_idx)
        chn_handle = zlg_start_channel(zcanlib, dev_handle, args.chan, args.abit, args.dbit, loopback=bool(args.loopback))
        logging.info("Device handle=%s, Channel handle=%s", dev_handle, chn_handle)
    else:
        logging.info("Dry-run: zlgcan not required; will not open device")

    srv = ZlgSimServer(zcanlib, dev_handle, chn_handle, parsers_by_id, cfg, dry_run=bool(args.dry_run))

    def _stop(signum, frame):
        logging.info("Signal %s received, stopping...", signum)
        srv.stop()
        try:
            if chn_handle is not None and zcanlib is not None:
                zcanlib.ZCAN().ResetCAN(chn_handle)
            if dev_handle is not None and zcanlib is not None:
                zcanlib.ZCAN().CloseDevice(dev_handle)
        except Exception:
            pass
        sys.exit(0)

    for s in (signal.SIGINT, signal.SIGTERM):
        try: signal.signal(s, _stop)
        except Exception: pass

    srv.start()
    while True: time.sleep(1)

if __name__ == "__main__":
    raise SystemExit(main())
