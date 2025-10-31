from . import generate_0x117 as g
CAN_ID = 0x117

def parse_frame(can_id, data):
    if can_id != CAN_ID:
        return {}
    m = g.decode_0x117_can_msg(data)
    out = {}
    for f in getattr(m, "__dataclass_fields__", {}):
        out[f] = getattr(m, f)
    return out

def encode_signals(updates):
    msg = g.canfd_0x117_msg()
    for k, v in updates.items():
        if hasattr(msg, k):
            try:
                setattr(msg, k, v)
            except Exception:
                pass
    payload = bytes(g.generate_0x117_can_msg_bytes(msg))
    return [(CAN_ID, payload)]
