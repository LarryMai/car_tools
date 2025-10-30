#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZLG USBCANFD RX Sniffer
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

    if lib.StartCAN(ch) != getattr(zlgcan, "ZCAN_STATUS_OK", 1):
        raise SystemExit("[ERR] StartCAN failed")
    return ch

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="USBCANFD RX sniffer")
    p.add_argument("--dev-type", default="USBCANFD_100U")
    p.add_argument("--dev-idx", type=int, default=0)
    p.add_argument("--chan", type=int, default=0)
    p.add_argument("--abit", type=int, default=500000)
    p.add_argument("--dbit", type=int, default=2000000)
    p.add_argument("--loopback", action="store_true")
    return p.parse_args()

def main() -> int:
    args = parse_args()
    dev = open_device(args.dev_type, args.dev_idx)
    chn = start_channel(dev, args.chan, args.abit, args.dbit, loopback=bool(args.loopback))
    lib = zlgcan.ZCAN()
    print(f"[INFO] Sniffing dev={dev} chn={chn}  (Ctrl+C to stop)")

    try:
        while True:
            num_fd = lib.GetReceiveNum(chn, getattr(zlgcan, "ZCAN_TYPE_CANFD", 1))
            if num_fd:
                take = min(num_fd, 256)
                arr, got = lib.ReceiveFD(chn, take, 50)
                for i in range(got):
                    f = arr[i].frame
                    can_id = f.can_id & 0x1FFFFFFF
                    dl = int(f.len)
                    data = bytes(f.data[:dl])
                    brs = bool(f.flags & 0x01)
                    print(f"[RX-FD] id=0x{can_id:X} len={dl} brs={brs} data={data.hex(' ')}")

            num = lib.GetReceiveNum(chn, getattr(zlgcan, "ZCAN_TYPE_CAN", 0))
            if num:
                take = min(num, 256)
                arr, got = lib.Receive(chn, take, 50)
                for i in range(got):
                    f = arr[i].frame
                    can_id = f.can_id & 0x1FFFFFFF
                    dlc = int(f.can_dlc)
                    data = bytes(f.data[:dlc])
                    print(f"[RX]    id=0x{can_id:X} dlc={dlc} data={data.hex(' ')}")

            time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            lib.ResetCAN(chn)
        except Exception:
            pass
        try:
            zlgcan.ZCAN().CloseDevice(dev)
        except Exception:
            pass
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
