#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, sys, os, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if hasattr(os, "add_dll_directory"):
    try:
        os.add_dll_directory(str(HERE))
        os.add_dll_directory(str(HERE / "kerneldlls"))
    except Exception:
        pass

import zlgcan  # type: ignore

def _dev_map():
    m = {}
    for k in [
        "ZCAN_USBCANFD_100U",
        "ZCAN_USBCANFD_100U_MINI",
        "ZCAN_USBCANFD_200U",
        "ZCAN_USBCANFD_400U",
        "ZCAN_USBCANFD_800U",
    ]:
        v = getattr(zlgcan, k, None)
        if v is not None:
            m[k.replace("ZCAN_", "")] = v
    return m

def open_dev(kind, idx):
    dt = _dev_map().get(kind.upper())
    if dt is None:
        raise SystemExit(f"Unsupported dev-type: {kind}")
    h = zlgcan.ZCAN().OpenDevice(dt, idx, 0)
    if h == getattr(zlgcan, "INVALID_DEVICE_HANDLE", 0):
        raise SystemExit("OpenDevice failed")
    return h

def start_chan(dev, ch, abit, dbit, loopback=True, tx_echo=True):
    lib = zlgcan.ZCAN()
    # bitrate
    lib.ZCAN_SetValue(dev, f"{ch}/canfd_abit_baud_rate", str(abit).encode())
    lib.ZCAN_SetValue(dev, f"{ch}/canfd_dbit_baud_rate", str(dbit).encode())
    # terminator (ignore errors if not supported)
    try: 
        lib.ZCAN_SetValue(dev, f"{ch}/initenal_resistance", b"1")
    except Exception: pass
    # init as CAN FD
    cfg = zlgcan.ZCAN_CHANNEL_INIT_CONFIG()
    cfg.can_type = getattr(zlgcan, "ZCAN_TYPE_CANFD", 1)
    cfg.config.canfd.mode = 1 if loopback else 0
    chn = lib.InitCAN(dev, ch, cfg)
    if chn is None: 
        raise SystemExit("InitCAN failed")
    
    # tx echo (ignore if not supported)
    if tx_echo:
        try: 
            lib.ZCAN_SetValue(dev, f"{ch}/set_device_tx_echo", b"1")
        except Exception: pass
    if lib.StartCAN(chn) != getattr(zlgcan, "ZCAN_STATUS_OK", 1):
        raise SystemExit("StartCAN failed")
    return chn

def hx(s: str) -> bytes:
    s = s.strip().replace(" ", "")
    s = s[2:] if s.startswith("0x") else s
    if len(s) % 2:
        s = "0" + s
    return bytes.fromhex(s)

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("single-channel loopback TX/RX self-test (param batch)")
    p.add_argument("--dev-type", default="USBCANFD_100U")
    p.add_argument("--dev-idx", type=int, default=0)
    p.add_argument("--chan", type=int, default=0)
    p.add_argument("--abit", type=int, default=500000)
    p.add_argument("--dbit", type=int, default=2000000)
    p.add_argument("--id", required=True, help="e.g. 0x117")
    p.add_argument("--data", default="DE AD BE EF")
    p.add_argument("--fd", action="store_true")
    p.add_argument("--brs", action="store_true")
    p.add_argument("--period-ms", type=int, default=500)
    # NEW: batch sizes
    p.add_argument("--rx-batch-fd", type=int, default=64, help="FD receive batch size per call")
    p.add_argument("--rx-batch", type=int, default=128, help="Classic CAN receive batch size per call")
    return p.parse_args()

def main() -> int:
    a = parse_args()
    can_id = int(a.id, 0)
    payload = hx(a.data)
    dev = open_dev(a.dev_type, a.dev_idx)
    chn = start_chan(dev, a.chan, a.abit, a.dbit, loopback=True, tx_echo=True)
    lib = zlgcan.ZCAN()
    print(f"[INFO] dev={dev} chn={chn} FD={a.fd} BRS={a.brs} loopback=ON echo=ON "
          f"batchFD={a.rx_batch_fd} batch={a.rx_batch}")

    t0 = 0.0
    try:
        while True:
            now = time.time()
            if now - t0 >= (a.period_ms / 1000.0):
                if a.fd or len(payload) > 8:
                    obj = zlgcan.ZCAN_TransmitFD_Data()
                    obj.transmit_type = 0
                    obj.frame.can_id = can_id | (1 << 31 if can_id > 0x7FF else 0)
                    obj.frame.len = len(payload)
                    if a.brs:
                        obj.frame.flags |= 0x1
                    for i, b in enumerate(payload): obj.frame.data[i] = b
                    lib.TransmitFD(chn, (zlgcan.ZCAN_TransmitFD_Data * 1)(obj), 1)
                else:
                    obj = zlgcan.ZCAN_Transmit_Data()
                    obj.transmit_type = 0
                    obj.frame.can_id = can_id | (1 << 31 if can_id > 0x7FF else 0)
                    obj.frame.can_dlc = len(payload)
                    for i, b in enumerate(payload):
                        obj.frame.data[i] = b
                    lib.Transmit(chn, (zlgcan.ZCAN_Transmit_Data * 1)(obj), 1)
                print(f"[TX] id=0x{can_id:X} data={payload.hex(' ')}")
                t0 = now

                # Read-back once after TX (grab echo/loopback)
                time.sleep(0.01)
                # FD
                nfd = lib.GetReceiveNum(chn, getattr(zlgcan, "ZCAN_TYPE_CANFD", 1))
                if nfd:
                    arr, got = lib.ReceiveFD(chn, min(nfd, max(1, a.rx_batch_fd)), 10)
                    for i in range(got):
                        f = arr[i].frame
                        dl = int(f.len)
                        print(f"[RX-FD] id=0x{f.can_id & 0x1FFFFFFF:X} len={dl} brs={bool(f.flags & 1)} "
                              f"data={bytes(f.data[:dl]).hex(' ')}")
                # Classic
                n = lib.GetReceiveNum(chn, getattr(zlgcan, "ZCAN_TYPE_CAN", 0))
                if n:
                    arr, got = lib.Receive(chn, min(n, max(1, a.rx_batch)), 10)
                    for i in range(got):
                        f = arr[i].frame
                        dlc = int(f.can_dlc)
                        print(f"[RX]    id=0x{f.can_id & 0x1FFFFFFF:X} dlc={dlc} "
                              f"data={bytes(f.data[:dlc]).hex(' ')}")

            time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        try: 
            lib.ResetCAN(chn)
        except Exception: pass
        try: 
            zlgcan.ZCAN().CloseDevice(dev)
        except Exception: pass
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
