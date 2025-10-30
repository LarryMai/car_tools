#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZLG USBCANFD TX Tester
- 放在 examples/ 與 zlgcan.py/zlgcan.dll/kerneldlls/ 同層
"""
from __future__ import annotations
import argparse, sys, os, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if hasattr(os, "add_dll_directory"):
    try: os.add_dll_directory(str(HERE))
    except Exception: pass
    kd = HERE / "kerneldlls"
    if kd.exists():
        try: os.add_dll_directory(str(kd))
        except Exception: pass

import zlgcan  # type: ignore

def _build_dev_map() -> dict[str, int]:
    names = [
        "ZCAN_USBCANFD_100U",
        "ZCAN_USBCANFD_100U_MINI",
        "ZCAN_USBCANFD_200U",
        "ZCAN_USBCANFD_400U",
        "ZCAN_USBCANFD_800U",
    ]
    dev_map = {}
    for nm in names:
        v = getattr(zlgcan, nm, None)
        if v is not None:
            dev_map[nm.replace("ZCAN_", "")] = v
    return dev_map

def open_device(dev_type_key: str, dev_idx: int) -> int:
    dev_map = _build_dev_map()
    dtype = dev_map.get(dev_type_key.upper())
    if dtype is None:
        raise SystemExit(f"[ERR] Unsupported dev type '{dev_type_key}'. Available: {list(dev_map.keys())}")
    lib = zlgcan.ZCAN()
    h = lib.OpenDevice(dtype, dev_idx, 0)
    if h == getattr(zlgcan, "INVALID_DEVICE_HANDLE", 0):
        raise SystemExit("[ERR] OpenDevice failed")
    return h

def start_channel(dev_handle: int, chn: int, abit: int, dbit: int, loopback: bool=False) -> int:
    lib = zlgcan.ZCAN()
    ok = lib.ZCAN_SetValue(dev_handle, f"{chn}/canfd_abit_baud_rate", str(abit).encode("utf-8"))
    if ok != getattr(zlgcan, "ZCAN_STATUS_OK", 1):
        raise SystemExit("[ERR] Set arbitration bitrate failed")
    ok = lib.ZCAN_SetValue(dev_handle, f"{chn}/canfd_dbit_baud_rate", str(dbit).encode("utf-8"))
    if ok != getattr(zlgcan, "ZCAN_STATUS_OK", 1):
        raise SystemExit("[ERR] Set data bitrate failed")

    try:
        lib.ZCAN_SetValue(dev_handle, f"{chn}/initenal_resistance", b"1")
    except Exception:
        pass

    cfg = zlgcan.ZCAN_CHANNEL_INIT_CONFIG()
    cfg.can_type = getattr(zlgcan, "ZCAN_TYPE_CANFD", 1)
    cfg.config.canfd.mode = 1 if loopback else 0

    ch = lib.InitCAN(dev_handle, chn, cfg)
    if ch is None:
        raise SystemExit("[ERR] InitCAN failed")

    try:
        lib.ZCAN_SetValue(dev_handle, f"{chn}/set_device_tx_echo", b"0")
    except Exception:
        pass

    if lib.StartCAN(ch) != getattr(zlgcan, "ZCAN_STATUS_OK", 1):
        raise SystemExit("[ERR] StartCAN failed")
    return ch

def hex_to_bytes(s: str) -> bytes:
    s = s.strip().replace(" ", "")
    if s.startswith("0x") and len(s) > 2:
        s = s[2:]
    if len(s) % 2 != 0:
        s = "0" + s
    return bytes.fromhex(s)

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="USBCANFD TX tester")
    p.add_argument("--dev-type", default="USBCANFD_100U", help="USBCANFD_100U|USBCANFD_200U|USBCANFD_400U|USBCANFD_800U|...")
    p.add_argument("--dev-idx", type=int, default=0)
    p.add_argument("--chan", type=int, default=0)
    p.add_argument("--abit", type=int, default=500000)
    p.add_argument("--dbit", type=int, default=2000000)
    p.add_argument("--id", required=True, help="CAN ID, e.g. 0x117 or 279")
    p.add_argument("--data", default="00", help='payload hex, e.g. "11 22 33 44" or "0x11223344"')
    p.add_argument("--period-ms", type=int, default=1000, help="send period; if 0, send once")
    p.add_argument("--count", type=int, default=0, help="send N frames then exit; 0 means infinite")
    p.add_argument("--extended", action="store_true", help="use extended ID (EFF)")
    p.add_argument("--fd", action="store_true", help="send as CAN FD frame")
    p.add_argument("--brs", action="store_true", help="FD bit rate switch (BRS)")
    p.add_argument("--loopback", action="store_true", help="controller loopback mode")
    return p.parse_args()

def main() -> int:
    args = parse_args()
    can_id = int(args.id, 0)
    data = hex_to_bytes(args.data)
    if not (0 <= len(data) <= 64):
        raise SystemExit("[ERR] payload bytes must be 0..64 for FD (0..8 for classic)")

    dev = open_device(args.dev_type, args.dev_idx)
    chn = start_channel(dev, args.chan, args.abit, args.dbit, loopback=bool(args.loopback))
    lib = zlgcan.ZCAN()

    print(f"[INFO] Open OK dev={dev} chn={chn}  FD={args.fd} BRS={args.brs} EXT={args.extended}")
    sent = 0
    try:
        while True:
            if args.fd or len(data) > 8:
                obj = zlgcan.ZCAN_TransmitFD_Data()
                obj.transmit_type = 0
                obj.frame.can_id = can_id | (1<<31 if (args.extended or can_id > 0x7FF) else 0)
                obj.frame.len = len(data)
                if args.brs:
                    obj.frame.flags |= 0x1  # BRS
                for i, b in enumerate(data):
                    obj.frame.data[i] = b
                lib.TransmitFD(chn, (zlgcan.ZCAN_TransmitFD_Data * 1)(obj), 1)
            else:
                obj = zlgcan.ZCAN_Transmit_Data()
                obj.transmit_type = 0
                obj.frame.can_id = can_id | (1<<31 if (args.extended or can_id > 0x7FF) else 0)
                obj.frame.can_dlc = len(data)
                for i, b in enumerate(data):
                    obj.frame.data[i] = b
                lib.Transmit(chn, (zlgcan.ZCAN_Transmit_Data * 1)(obj), 1)

            sent += 1
            print(f"[TX] id=0x{can_id:X} len={len(data)} data={data.hex(' ')} count={sent}")
            if args.period_ms <= 0:
                break
            if args.count and sent >= args.count:
                break
            time.sleep(args.period_ms / 1000.0)
        return 0
    finally:
        try:
            lib.ResetCAN(chn)
        except Exception:
            pass
        try:
            zlgcan.ZCAN().CloseDevice(dev)
        except Exception:
            pass

if __name__ == "__main__":
    raise SystemExit(main())
