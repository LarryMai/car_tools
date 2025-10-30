# ================================================
#  Auto-generated CAN Message Encoder/Decoder (with Enums)
#  Source DBC : FPD1_102.4_CAN2_Meter_20250805_Fix.dbc
#  DBC Version: 20250805
#  Generated  : 2025-10-29 14:39:39
# ================================================

from typing import Dict, List, Tuple
import re

STRICT_ENUM = False  # loose by default; set True to raise on unknown enum values
def to_enum(cls, value, strict: bool = False):
    """Cast integer to IntEnum; if strict=False and value is unknown, return the raw int."""
    try:
        return cls(int(value))
    except Exception:
        if strict:
            raise
        return int(value)

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

from enum import IntEnum

class ShiftGearPosnEnum(IntEnum):
    PARK = 0
    INVALID = 1
    RESERVED_2 = 2
    RESERVED_3 = 3
    NEUTRAL = 4
    DRIVE = 5
    FAILURE = 6
    REVERSE = 7

class PwrStaEnum(IntEnum):
    OFF = 0
    OFF_CHARGING = 1
    OFF_AFTER_RUN = 2
    STANDBY = 3
    ON = 4
    READY = 5
    INVALID = 7

class EDriveSysErr_VCUErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class EDriveSysErr_AccPedalErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class FD_Telltale_FailEnum(IntEnum):
    NORMAL = 0
    TELLTALE_FAIL = 1

class FD_TCS_IndicatorEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_Steering_WarningEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_ABS_WarningEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_Battery_Charge_WarningEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_EDrive_SystemEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_EPB_ErrorEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_HV_Battery_FaultEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_Park_Brake_WarningEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class FD_Power_limitationEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class LimphomeActEnum(IntEnum):
    INACTIVE = 0
    ACTIVE = 1

class EDriveSysErr_MCUErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class HVSysErr_RelayErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class HVSysErr_PackErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class HVSysErr_IsolationErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class PwrStaErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class LVSysErr_PwrOutpErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class EDriveSysErr_ShifterErrEnum(IntEnum):
    NORMAL = 0
    ERROR = 1

class FD_EBMErrStaEnum(IntEnum):
    OFF = 0
    ON = 1
    FLASH = 2

class LTurnLPEnum(IntEnum):
    OFF = 0
    ON = 1

class RTurnLPEnum(IntEnum):
    OFF = 0
    ON = 1

class FDC_VCU_LVStaTooLow_StaEnum(IntEnum):
    NORMAL = 0
    LV_STATE_TOO_LOW = 1

class FDC_VCU_LVStaDropQuick_StaEnum(IntEnum):
    NORMAL = 0
    LV_STATE_DROP_QUICKLY = 1

class FDC_VCU_LVChrgFreq_StaEnum(IntEnum):
    NORMAL = 0
    SILENT_CHARGE_FREQUENTLY_LV1 = 1
    SILENT_CHARGE_FREQUENTLY_LV2 = 2

# Message: FD2_CE100_0 (ID=0x117, DLC=64)

ShiftGearPosn_OFFSET = 37
ShiftGearPosn_LEN = 3
ShiftGearPosn_BYTE_ORDER = 'big_endian'
PwrSta_OFFSET = 34
PwrSta_LEN = 3
PwrSta_BYTE_ORDER = 'big_endian'
EDriveSysErr_VCUErr_OFFSET = 142
EDriveSysErr_VCUErr_LEN = 1
EDriveSysErr_VCUErr_BYTE_ORDER = 'big_endian'
EDriveSysErr_AccPedalErr_OFFSET = 141
EDriveSysErr_AccPedalErr_LEN = 1
EDriveSysErr_AccPedalErr_BYTE_ORDER = 'big_endian'
MeterIndSpeed_raw32_OFFSET = 151
MeterIndSpeed_raw32_LEN = 8
MeterIndSpeed_raw32_BYTE_ORDER = 'big_endian'
FD_Telltale_Fail_OFFSET = 164
FD_Telltale_Fail_LEN = 1
FD_Telltale_Fail_BYTE_ORDER = 'big_endian'
FD_TCS_Indicator_OFFSET = 163
FD_TCS_Indicator_LEN = 2
FD_TCS_Indicator_BYTE_ORDER = 'big_endian'
FD_Steering_Warning_OFFSET = 161
FD_Steering_Warning_LEN = 2
FD_Steering_Warning_BYTE_ORDER = 'big_endian'
FD_ABS_Warning_OFFSET = 183
FD_ABS_Warning_LEN = 2
FD_ABS_Warning_BYTE_ORDER = 'big_endian'
FD_Battery_Charge_Warning_OFFSET = 181
FD_Battery_Charge_Warning_LEN = 2
FD_Battery_Charge_Warning_BYTE_ORDER = 'big_endian'
FD_EDrive_System_OFFSET = 179
FD_EDrive_System_LEN = 2
FD_EDrive_System_BYTE_ORDER = 'big_endian'
FD_EPB_Error_OFFSET = 177
FD_EPB_Error_LEN = 2
FD_EPB_Error_BYTE_ORDER = 'big_endian'
FD_HV_Battery_Fault_OFFSET = 191
FD_HV_Battery_Fault_LEN = 2
FD_HV_Battery_Fault_BYTE_ORDER = 'big_endian'
FD_Park_Brake_Warning_OFFSET = 189
FD_Park_Brake_Warning_LEN = 2
FD_Park_Brake_Warning_BYTE_ORDER = 'big_endian'
FD_Power_limitation_OFFSET = 187
FD_Power_limitation_LEN = 2
FD_Power_limitation_BYTE_ORDER = 'big_endian'
LimphomeAct_OFFSET = 207
LimphomeAct_LEN = 1
LimphomeAct_BYTE_ORDER = 'big_endian'
EDriveSysErr_MCUErr_OFFSET = 203
EDriveSysErr_MCUErr_LEN = 1
EDriveSysErr_MCUErr_BYTE_ORDER = 'big_endian'
HVSysErr_RelayErr_OFFSET = 212
HVSysErr_RelayErr_LEN = 1
HVSysErr_RelayErr_BYTE_ORDER = 'big_endian'
HVSysErr_PackErr_OFFSET = 211
HVSysErr_PackErr_LEN = 1
HVSysErr_PackErr_BYTE_ORDER = 'big_endian'
HVSysErr_IsolationErr_OFFSET = 210
HVSysErr_IsolationErr_LEN = 1
HVSysErr_IsolationErr_BYTE_ORDER = 'big_endian'
PwrStaErr_OFFSET = 209
PwrStaErr_LEN = 1
PwrStaErr_BYTE_ORDER = 'big_endian'
LVSysErr_PwrOutpErr_OFFSET = 208
LVSysErr_PwrOutpErr_LEN = 1
LVSysErr_PwrOutpErr_BYTE_ORDER = 'big_endian'
EDriveSysErr_ShifterErr_OFFSET = 223
EDriveSysErr_ShifterErr_LEN = 1
EDriveSysErr_ShifterErr_BYTE_ORDER = 'big_endian'
FD_EBMErrSta_OFFSET = 221
FD_EBMErrSta_LEN = 2
FD_EBMErrSta_BYTE_ORDER = 'big_endian'
LTurnLP_OFFSET = 246
LTurnLP_LEN = 1
LTurnLP_BYTE_ORDER = 'big_endian'
RTurnLP_OFFSET = 245
RTurnLP_LEN = 1
RTurnLP_BYTE_ORDER = 'big_endian'
FDC_VCU_LVStaTooLow_Sta_OFFSET = 304
FDC_VCU_LVStaTooLow_Sta_LEN = 1
FDC_VCU_LVStaTooLow_Sta_BYTE_ORDER = 'big_endian'
FDC_VCU_LVStaDropQuick_Sta_OFFSET = 312
FDC_VCU_LVStaDropQuick_Sta_LEN = 1
FDC_VCU_LVStaDropQuick_Sta_BYTE_ORDER = 'big_endian'
FDC_VCU_LVChrgFreq_Sta_OFFSET = 325
FDC_VCU_LVChrgFreq_Sta_LEN = 2
FDC_VCU_LVChrgFreq_Sta_BYTE_ORDER = 'big_endian'

from dataclasses import dataclass

@dataclass
class canfd_0x117_msg:
    ShiftGearPosn: ShiftGearPosnEnum = ShiftGearPosnEnum.PARK
    PwrSta: PwrStaEnum = PwrStaEnum.OFF
    EDriveSysErr_VCUErr: EDriveSysErr_VCUErrEnum = EDriveSysErr_VCUErrEnum.NORMAL
    EDriveSysErr_AccPedalErr: EDriveSysErr_AccPedalErrEnum = EDriveSysErr_AccPedalErrEnum.NORMAL
    MeterIndSpeed_raw32: int = 0
    FD_Telltale_Fail: FD_Telltale_FailEnum = FD_Telltale_FailEnum.NORMAL
    FD_TCS_Indicator: FD_TCS_IndicatorEnum = FD_TCS_IndicatorEnum.OFF
    FD_Steering_Warning: FD_Steering_WarningEnum = FD_Steering_WarningEnum.OFF
    FD_ABS_Warning: FD_ABS_WarningEnum = FD_ABS_WarningEnum.OFF
    FD_Battery_Charge_Warning: FD_Battery_Charge_WarningEnum = FD_Battery_Charge_WarningEnum.OFF
    FD_EDrive_System: FD_EDrive_SystemEnum = FD_EDrive_SystemEnum.OFF
    FD_EPB_Error: FD_EPB_ErrorEnum = FD_EPB_ErrorEnum.OFF
    FD_HV_Battery_Fault: FD_HV_Battery_FaultEnum = FD_HV_Battery_FaultEnum.OFF
    FD_Park_Brake_Warning: FD_Park_Brake_WarningEnum = FD_Park_Brake_WarningEnum.OFF
    FD_Power_limitation: FD_Power_limitationEnum = FD_Power_limitationEnum.OFF
    LimphomeAct: LimphomeActEnum = LimphomeActEnum.INACTIVE
    EDriveSysErr_MCUErr: EDriveSysErr_MCUErrEnum = EDriveSysErr_MCUErrEnum.NORMAL
    HVSysErr_RelayErr: HVSysErr_RelayErrEnum = HVSysErr_RelayErrEnum.NORMAL
    HVSysErr_PackErr: HVSysErr_PackErrEnum = HVSysErr_PackErrEnum.NORMAL
    HVSysErr_IsolationErr: HVSysErr_IsolationErrEnum = HVSysErr_IsolationErrEnum.NORMAL
    PwrStaErr: PwrStaErrEnum = PwrStaErrEnum.NORMAL
    LVSysErr_PwrOutpErr: LVSysErr_PwrOutpErrEnum = LVSysErr_PwrOutpErrEnum.NORMAL
    EDriveSysErr_ShifterErr: EDriveSysErr_ShifterErrEnum = EDriveSysErr_ShifterErrEnum.NORMAL
    FD_EBMErrSta: FD_EBMErrStaEnum = FD_EBMErrStaEnum.OFF
    LTurnLP: LTurnLPEnum = LTurnLPEnum.OFF
    RTurnLP: RTurnLPEnum = RTurnLPEnum.OFF
    FDC_VCU_LVStaTooLow_Sta: FDC_VCU_LVStaTooLow_StaEnum = FDC_VCU_LVStaTooLow_StaEnum.NORMAL
    FDC_VCU_LVStaDropQuick_Sta: FDC_VCU_LVStaDropQuick_StaEnum = FDC_VCU_LVStaDropQuick_StaEnum.NORMAL
    FDC_VCU_LVChrgFreq_Sta: FDC_VCU_LVChrgFreq_StaEnum = FDC_VCU_LVChrgFreq_StaEnum.NORMAL

def generate_0x117_can_msg_bytes(msg: canfd_0x117_msg, debug: bool = False) -> List[int]:
    data = bytearray(64)
    shiftgearposn = int(msg.ShiftGearPosn)
    if ShiftGearPosn_BYTE_ORDER == 'little_endian':
        for i in range(ShiftGearPosn_LEN):
            bit_pos = ShiftGearPosn_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (shiftgearposn >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode ShiftGearPosn: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(ShiftGearPosn_OFFSET, ShiftGearPosn_LEN)):
            bit_val = (shiftgearposn >> (ShiftGearPosn_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode ShiftGearPosn: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    pwrsta = int(msg.PwrSta)
    if PwrSta_BYTE_ORDER == 'little_endian':
        for i in range(PwrSta_LEN):
            bit_pos = PwrSta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (pwrsta >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode PwrSta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(PwrSta_OFFSET, PwrSta_LEN)):
            bit_val = (pwrsta >> (PwrSta_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode PwrSta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    edrivesyserr_vcuerr = int(msg.EDriveSysErr_VCUErr)
    if EDriveSysErr_VCUErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_VCUErr_LEN):
            bit_pos = EDriveSysErr_VCUErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (edrivesyserr_vcuerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_VCUErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_VCUErr_OFFSET, EDriveSysErr_VCUErr_LEN)):
            bit_val = (edrivesyserr_vcuerr >> (EDriveSysErr_VCUErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_VCUErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    edrivesyserr_accpedalerr = int(msg.EDriveSysErr_AccPedalErr)
    if EDriveSysErr_AccPedalErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_AccPedalErr_LEN):
            bit_pos = EDriveSysErr_AccPedalErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (edrivesyserr_accpedalerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_AccPedalErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_AccPedalErr_OFFSET, EDriveSysErr_AccPedalErr_LEN)):
            bit_val = (edrivesyserr_accpedalerr >> (EDriveSysErr_AccPedalErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_AccPedalErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    meterindspeed_raw32 = msg.MeterIndSpeed_raw32
    if MeterIndSpeed_raw32_BYTE_ORDER == 'little_endian':
        for i in range(MeterIndSpeed_raw32_LEN):
            bit_pos = MeterIndSpeed_raw32_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (meterindspeed_raw32 >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode MeterIndSpeed_raw32: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(MeterIndSpeed_raw32_OFFSET, MeterIndSpeed_raw32_LEN)):
            bit_val = (meterindspeed_raw32 >> (MeterIndSpeed_raw32_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode MeterIndSpeed_raw32: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_telltale_fail = int(msg.FD_Telltale_Fail)
    if FD_Telltale_Fail_BYTE_ORDER == 'little_endian':
        for i in range(FD_Telltale_Fail_LEN):
            bit_pos = FD_Telltale_Fail_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_telltale_fail >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Telltale_Fail: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Telltale_Fail_OFFSET, FD_Telltale_Fail_LEN)):
            bit_val = (fd_telltale_fail >> (FD_Telltale_Fail_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Telltale_Fail: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_tcs_indicator = int(msg.FD_TCS_Indicator)
    if FD_TCS_Indicator_BYTE_ORDER == 'little_endian':
        for i in range(FD_TCS_Indicator_LEN):
            bit_pos = FD_TCS_Indicator_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_tcs_indicator >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_TCS_Indicator: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_TCS_Indicator_OFFSET, FD_TCS_Indicator_LEN)):
            bit_val = (fd_tcs_indicator >> (FD_TCS_Indicator_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_TCS_Indicator: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_steering_warning = int(msg.FD_Steering_Warning)
    if FD_Steering_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Steering_Warning_LEN):
            bit_pos = FD_Steering_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_steering_warning >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Steering_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Steering_Warning_OFFSET, FD_Steering_Warning_LEN)):
            bit_val = (fd_steering_warning >> (FD_Steering_Warning_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Steering_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_abs_warning = int(msg.FD_ABS_Warning)
    if FD_ABS_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_ABS_Warning_LEN):
            bit_pos = FD_ABS_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_abs_warning >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_ABS_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_ABS_Warning_OFFSET, FD_ABS_Warning_LEN)):
            bit_val = (fd_abs_warning >> (FD_ABS_Warning_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_ABS_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_battery_charge_warning = int(msg.FD_Battery_Charge_Warning)
    if FD_Battery_Charge_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Battery_Charge_Warning_LEN):
            bit_pos = FD_Battery_Charge_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_battery_charge_warning >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Battery_Charge_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Battery_Charge_Warning_OFFSET, FD_Battery_Charge_Warning_LEN)):
            bit_val = (fd_battery_charge_warning >> (FD_Battery_Charge_Warning_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Battery_Charge_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_edrive_system = int(msg.FD_EDrive_System)
    if FD_EDrive_System_BYTE_ORDER == 'little_endian':
        for i in range(FD_EDrive_System_LEN):
            bit_pos = FD_EDrive_System_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_edrive_system >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EDrive_System: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EDrive_System_OFFSET, FD_EDrive_System_LEN)):
            bit_val = (fd_edrive_system >> (FD_EDrive_System_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EDrive_System: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_epb_error = int(msg.FD_EPB_Error)
    if FD_EPB_Error_BYTE_ORDER == 'little_endian':
        for i in range(FD_EPB_Error_LEN):
            bit_pos = FD_EPB_Error_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_epb_error >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EPB_Error: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EPB_Error_OFFSET, FD_EPB_Error_LEN)):
            bit_val = (fd_epb_error >> (FD_EPB_Error_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EPB_Error: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_hv_battery_fault = int(msg.FD_HV_Battery_Fault)
    if FD_HV_Battery_Fault_BYTE_ORDER == 'little_endian':
        for i in range(FD_HV_Battery_Fault_LEN):
            bit_pos = FD_HV_Battery_Fault_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_hv_battery_fault >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_HV_Battery_Fault: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_HV_Battery_Fault_OFFSET, FD_HV_Battery_Fault_LEN)):
            bit_val = (fd_hv_battery_fault >> (FD_HV_Battery_Fault_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_HV_Battery_Fault: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_park_brake_warning = int(msg.FD_Park_Brake_Warning)
    if FD_Park_Brake_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Park_Brake_Warning_LEN):
            bit_pos = FD_Park_Brake_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_park_brake_warning >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Park_Brake_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Park_Brake_Warning_OFFSET, FD_Park_Brake_Warning_LEN)):
            bit_val = (fd_park_brake_warning >> (FD_Park_Brake_Warning_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Park_Brake_Warning: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_power_limitation = int(msg.FD_Power_limitation)
    if FD_Power_limitation_BYTE_ORDER == 'little_endian':
        for i in range(FD_Power_limitation_LEN):
            bit_pos = FD_Power_limitation_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_power_limitation >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Power_limitation: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Power_limitation_OFFSET, FD_Power_limitation_LEN)):
            bit_val = (fd_power_limitation >> (FD_Power_limitation_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_Power_limitation: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    limphomeact = int(msg.LimphomeAct)
    if LimphomeAct_BYTE_ORDER == 'little_endian':
        for i in range(LimphomeAct_LEN):
            bit_pos = LimphomeAct_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (limphomeact >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LimphomeAct: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LimphomeAct_OFFSET, LimphomeAct_LEN)):
            bit_val = (limphomeact >> (LimphomeAct_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LimphomeAct: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    edrivesyserr_mcuerr = int(msg.EDriveSysErr_MCUErr)
    if EDriveSysErr_MCUErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_MCUErr_LEN):
            bit_pos = EDriveSysErr_MCUErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (edrivesyserr_mcuerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_MCUErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_MCUErr_OFFSET, EDriveSysErr_MCUErr_LEN)):
            bit_val = (edrivesyserr_mcuerr >> (EDriveSysErr_MCUErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_MCUErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    hvsyserr_relayerr = int(msg.HVSysErr_RelayErr)
    if HVSysErr_RelayErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_RelayErr_LEN):
            bit_pos = HVSysErr_RelayErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (hvsyserr_relayerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_RelayErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_RelayErr_OFFSET, HVSysErr_RelayErr_LEN)):
            bit_val = (hvsyserr_relayerr >> (HVSysErr_RelayErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_RelayErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    hvsyserr_packerr = int(msg.HVSysErr_PackErr)
    if HVSysErr_PackErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_PackErr_LEN):
            bit_pos = HVSysErr_PackErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (hvsyserr_packerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_PackErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_PackErr_OFFSET, HVSysErr_PackErr_LEN)):
            bit_val = (hvsyserr_packerr >> (HVSysErr_PackErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_PackErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    hvsyserr_isolationerr = int(msg.HVSysErr_IsolationErr)
    if HVSysErr_IsolationErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_IsolationErr_LEN):
            bit_pos = HVSysErr_IsolationErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (hvsyserr_isolationerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_IsolationErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_IsolationErr_OFFSET, HVSysErr_IsolationErr_LEN)):
            bit_val = (hvsyserr_isolationerr >> (HVSysErr_IsolationErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode HVSysErr_IsolationErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    pwrstaerr = int(msg.PwrStaErr)
    if PwrStaErr_BYTE_ORDER == 'little_endian':
        for i in range(PwrStaErr_LEN):
            bit_pos = PwrStaErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (pwrstaerr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode PwrStaErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(PwrStaErr_OFFSET, PwrStaErr_LEN)):
            bit_val = (pwrstaerr >> (PwrStaErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode PwrStaErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    lvsyserr_pwroutperr = int(msg.LVSysErr_PwrOutpErr)
    if LVSysErr_PwrOutpErr_BYTE_ORDER == 'little_endian':
        for i in range(LVSysErr_PwrOutpErr_LEN):
            bit_pos = LVSysErr_PwrOutpErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (lvsyserr_pwroutperr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LVSysErr_PwrOutpErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LVSysErr_PwrOutpErr_OFFSET, LVSysErr_PwrOutpErr_LEN)):
            bit_val = (lvsyserr_pwroutperr >> (LVSysErr_PwrOutpErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LVSysErr_PwrOutpErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    edrivesyserr_shiftererr = int(msg.EDriveSysErr_ShifterErr)
    if EDriveSysErr_ShifterErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_ShifterErr_LEN):
            bit_pos = EDriveSysErr_ShifterErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (edrivesyserr_shiftererr >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_ShifterErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_ShifterErr_OFFSET, EDriveSysErr_ShifterErr_LEN)):
            bit_val = (edrivesyserr_shiftererr >> (EDriveSysErr_ShifterErr_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode EDriveSysErr_ShifterErr: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fd_ebmerrsta = int(msg.FD_EBMErrSta)
    if FD_EBMErrSta_BYTE_ORDER == 'little_endian':
        for i in range(FD_EBMErrSta_LEN):
            bit_pos = FD_EBMErrSta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fd_ebmerrsta >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EBMErrSta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EBMErrSta_OFFSET, FD_EBMErrSta_LEN)):
            bit_val = (fd_ebmerrsta >> (FD_EBMErrSta_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FD_EBMErrSta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    lturnlp = int(msg.LTurnLP)
    if LTurnLP_BYTE_ORDER == 'little_endian':
        for i in range(LTurnLP_LEN):
            bit_pos = LTurnLP_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (lturnlp >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LTurnLP: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LTurnLP_OFFSET, LTurnLP_LEN)):
            bit_val = (lturnlp >> (LTurnLP_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode LTurnLP: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    rturnlp = int(msg.RTurnLP)
    if RTurnLP_BYTE_ORDER == 'little_endian':
        for i in range(RTurnLP_LEN):
            bit_pos = RTurnLP_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (rturnlp >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode RTurnLP: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(RTurnLP_OFFSET, RTurnLP_LEN)):
            bit_val = (rturnlp >> (RTurnLP_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode RTurnLP: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fdc_vcu_lvstatoolow_sta = int(msg.FDC_VCU_LVStaTooLow_Sta)
    if FDC_VCU_LVStaTooLow_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVStaTooLow_Sta_LEN):
            bit_pos = FDC_VCU_LVStaTooLow_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fdc_vcu_lvstatoolow_sta >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVStaTooLow_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVStaTooLow_Sta_OFFSET, FDC_VCU_LVStaTooLow_Sta_LEN)):
            bit_val = (fdc_vcu_lvstatoolow_sta >> (FDC_VCU_LVStaTooLow_Sta_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVStaTooLow_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fdc_vcu_lvstadropquick_sta = int(msg.FDC_VCU_LVStaDropQuick_Sta)
    if FDC_VCU_LVStaDropQuick_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVStaDropQuick_Sta_LEN):
            bit_pos = FDC_VCU_LVStaDropQuick_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fdc_vcu_lvstadropquick_sta >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVStaDropQuick_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVStaDropQuick_Sta_OFFSET, FDC_VCU_LVStaDropQuick_Sta_LEN)):
            bit_val = (fdc_vcu_lvstadropquick_sta >> (FDC_VCU_LVStaDropQuick_Sta_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVStaDropQuick_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    fdc_vcu_lvchrgfreq_sta = int(msg.FDC_VCU_LVChrgFreq_Sta)
    if FDC_VCU_LVChrgFreq_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVChrgFreq_Sta_LEN):
            bit_pos = FDC_VCU_LVChrgFreq_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (fdc_vcu_lvchrgfreq_sta >> i) & 1:
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVChrgFreq_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVChrgFreq_Sta_OFFSET, FDC_VCU_LVChrgFreq_Sta_LEN)):
            bit_val = (fdc_vcu_lvchrgfreq_sta >> (FDC_VCU_LVChrgFreq_Sta_LEN - 1 - i)) & 1
            if bit_val and 0 <= byte_i < len(data):
                before = data[byte_i]
                data[byte_i] |= (1 << bit_i)
                after = data[byte_i]
                if debug: print(f'Encode FDC_VCU_LVChrgFreq_Sta: byte{byte_i} bit {bit_i} → {before:#04x} → {after:#04x}')
    # Materialize to bytes for stable printing/return
    outb = bytes(data)
    if debug:
        print('[DEBUG] Encoded data bytes:', outb.hex(':'))
        print('[DEBUG] Encoded data list:', list(outb))
    return list(outb)

def decode_0x117_can_msg(data: bytes, debug: bool = False) -> canfd_0x117_msg:
    shiftgearposn = 0
    pwrsta = 0
    edrivesyserr_vcuerr = 0
    edrivesyserr_accpedalerr = 0
    meterindspeed_raw32 = 0
    fd_telltale_fail = 0
    fd_tcs_indicator = 0
    fd_steering_warning = 0
    fd_abs_warning = 0
    fd_battery_charge_warning = 0
    fd_edrive_system = 0
    fd_epb_error = 0
    fd_hv_battery_fault = 0
    fd_park_brake_warning = 0
    fd_power_limitation = 0
    limphomeact = 0
    edrivesyserr_mcuerr = 0
    hvsyserr_relayerr = 0
    hvsyserr_packerr = 0
    hvsyserr_isolationerr = 0
    pwrstaerr = 0
    lvsyserr_pwroutperr = 0
    edrivesyserr_shiftererr = 0
    fd_ebmerrsta = 0
    lturnlp = 0
    rturnlp = 0
    fdc_vcu_lvstatoolow_sta = 0
    fdc_vcu_lvstadropquick_sta = 0
    fdc_vcu_lvchrgfreq_sta = 0

    if ShiftGearPosn_BYTE_ORDER == 'little_endian':
        for i in range(ShiftGearPosn_LEN):
            bit_pos = ShiftGearPosn_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                shiftgearposn |= (1 << i)
                if debug: print(f'Decode ShiftGearPosn: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(ShiftGearPosn_OFFSET, ShiftGearPosn_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                shiftgearposn |= (1 << (ShiftGearPosn_LEN - 1 - i))
                if debug: print(f'Decode ShiftGearPosn: byte={byte_i}, bit={bit_i}, val=1')

    if PwrSta_BYTE_ORDER == 'little_endian':
        for i in range(PwrSta_LEN):
            bit_pos = PwrSta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                pwrsta |= (1 << i)
                if debug: print(f'Decode PwrSta: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(PwrSta_OFFSET, PwrSta_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                pwrsta |= (1 << (PwrSta_LEN - 1 - i))
                if debug: print(f'Decode PwrSta: byte={byte_i}, bit={bit_i}, val=1')

    if EDriveSysErr_VCUErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_VCUErr_LEN):
            bit_pos = EDriveSysErr_VCUErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_vcuerr |= (1 << i)
                if debug: print(f'Decode EDriveSysErr_VCUErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_VCUErr_OFFSET, EDriveSysErr_VCUErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_vcuerr |= (1 << (EDriveSysErr_VCUErr_LEN - 1 - i))
                if debug: print(f'Decode EDriveSysErr_VCUErr: byte={byte_i}, bit={bit_i}, val=1')

    if EDriveSysErr_AccPedalErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_AccPedalErr_LEN):
            bit_pos = EDriveSysErr_AccPedalErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_accpedalerr |= (1 << i)
                if debug: print(f'Decode EDriveSysErr_AccPedalErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_AccPedalErr_OFFSET, EDriveSysErr_AccPedalErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_accpedalerr |= (1 << (EDriveSysErr_AccPedalErr_LEN - 1 - i))
                if debug: print(f'Decode EDriveSysErr_AccPedalErr: byte={byte_i}, bit={bit_i}, val=1')

    if MeterIndSpeed_raw32_BYTE_ORDER == 'little_endian':
        for i in range(MeterIndSpeed_raw32_LEN):
            bit_pos = MeterIndSpeed_raw32_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                meterindspeed_raw32 |= (1 << i)
                if debug: print(f'Decode MeterIndSpeed_raw32: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(MeterIndSpeed_raw32_OFFSET, MeterIndSpeed_raw32_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                meterindspeed_raw32 |= (1 << (MeterIndSpeed_raw32_LEN - 1 - i))
                if debug: print(f'Decode MeterIndSpeed_raw32: byte={byte_i}, bit={bit_i}, val=1')

    if FD_Telltale_Fail_BYTE_ORDER == 'little_endian':
        for i in range(FD_Telltale_Fail_LEN):
            bit_pos = FD_Telltale_Fail_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_telltale_fail |= (1 << i)
                if debug: print(f'Decode FD_Telltale_Fail: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Telltale_Fail_OFFSET, FD_Telltale_Fail_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_telltale_fail |= (1 << (FD_Telltale_Fail_LEN - 1 - i))
                if debug: print(f'Decode FD_Telltale_Fail: byte={byte_i}, bit={bit_i}, val=1')

    if FD_TCS_Indicator_BYTE_ORDER == 'little_endian':
        for i in range(FD_TCS_Indicator_LEN):
            bit_pos = FD_TCS_Indicator_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_tcs_indicator |= (1 << i)
                if debug: print(f'Decode FD_TCS_Indicator: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_TCS_Indicator_OFFSET, FD_TCS_Indicator_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_tcs_indicator |= (1 << (FD_TCS_Indicator_LEN - 1 - i))
                if debug: print(f'Decode FD_TCS_Indicator: byte={byte_i}, bit={bit_i}, val=1')

    if FD_Steering_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Steering_Warning_LEN):
            bit_pos = FD_Steering_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_steering_warning |= (1 << i)
                if debug: print(f'Decode FD_Steering_Warning: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Steering_Warning_OFFSET, FD_Steering_Warning_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_steering_warning |= (1 << (FD_Steering_Warning_LEN - 1 - i))
                if debug: print(f'Decode FD_Steering_Warning: byte={byte_i}, bit={bit_i}, val=1')

    if FD_ABS_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_ABS_Warning_LEN):
            bit_pos = FD_ABS_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_abs_warning |= (1 << i)
                if debug: print(f'Decode FD_ABS_Warning: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_ABS_Warning_OFFSET, FD_ABS_Warning_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_abs_warning |= (1 << (FD_ABS_Warning_LEN - 1 - i))
                if debug: print(f'Decode FD_ABS_Warning: byte={byte_i}, bit={bit_i}, val=1')

    if FD_Battery_Charge_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Battery_Charge_Warning_LEN):
            bit_pos = FD_Battery_Charge_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_battery_charge_warning |= (1 << i)
                if debug: print(f'Decode FD_Battery_Charge_Warning: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Battery_Charge_Warning_OFFSET, FD_Battery_Charge_Warning_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_battery_charge_warning |= (1 << (FD_Battery_Charge_Warning_LEN - 1 - i))
                if debug: print(f'Decode FD_Battery_Charge_Warning: byte={byte_i}, bit={bit_i}, val=1')

    if FD_EDrive_System_BYTE_ORDER == 'little_endian':
        for i in range(FD_EDrive_System_LEN):
            bit_pos = FD_EDrive_System_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_edrive_system |= (1 << i)
                if debug: print(f'Decode FD_EDrive_System: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EDrive_System_OFFSET, FD_EDrive_System_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_edrive_system |= (1 << (FD_EDrive_System_LEN - 1 - i))
                if debug: print(f'Decode FD_EDrive_System: byte={byte_i}, bit={bit_i}, val=1')

    if FD_EPB_Error_BYTE_ORDER == 'little_endian':
        for i in range(FD_EPB_Error_LEN):
            bit_pos = FD_EPB_Error_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_epb_error |= (1 << i)
                if debug: print(f'Decode FD_EPB_Error: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EPB_Error_OFFSET, FD_EPB_Error_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_epb_error |= (1 << (FD_EPB_Error_LEN - 1 - i))
                if debug: print(f'Decode FD_EPB_Error: byte={byte_i}, bit={bit_i}, val=1')

    if FD_HV_Battery_Fault_BYTE_ORDER == 'little_endian':
        for i in range(FD_HV_Battery_Fault_LEN):
            bit_pos = FD_HV_Battery_Fault_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_hv_battery_fault |= (1 << i)
                if debug: print(f'Decode FD_HV_Battery_Fault: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_HV_Battery_Fault_OFFSET, FD_HV_Battery_Fault_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_hv_battery_fault |= (1 << (FD_HV_Battery_Fault_LEN - 1 - i))
                if debug: print(f'Decode FD_HV_Battery_Fault: byte={byte_i}, bit={bit_i}, val=1')

    if FD_Park_Brake_Warning_BYTE_ORDER == 'little_endian':
        for i in range(FD_Park_Brake_Warning_LEN):
            bit_pos = FD_Park_Brake_Warning_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_park_brake_warning |= (1 << i)
                if debug: print(f'Decode FD_Park_Brake_Warning: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Park_Brake_Warning_OFFSET, FD_Park_Brake_Warning_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_park_brake_warning |= (1 << (FD_Park_Brake_Warning_LEN - 1 - i))
                if debug: print(f'Decode FD_Park_Brake_Warning: byte={byte_i}, bit={bit_i}, val=1')

    if FD_Power_limitation_BYTE_ORDER == 'little_endian':
        for i in range(FD_Power_limitation_LEN):
            bit_pos = FD_Power_limitation_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_power_limitation |= (1 << i)
                if debug: print(f'Decode FD_Power_limitation: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_Power_limitation_OFFSET, FD_Power_limitation_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_power_limitation |= (1 << (FD_Power_limitation_LEN - 1 - i))
                if debug: print(f'Decode FD_Power_limitation: byte={byte_i}, bit={bit_i}, val=1')

    if LimphomeAct_BYTE_ORDER == 'little_endian':
        for i in range(LimphomeAct_LEN):
            bit_pos = LimphomeAct_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                limphomeact |= (1 << i)
                if debug: print(f'Decode LimphomeAct: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LimphomeAct_OFFSET, LimphomeAct_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                limphomeact |= (1 << (LimphomeAct_LEN - 1 - i))
                if debug: print(f'Decode LimphomeAct: byte={byte_i}, bit={bit_i}, val=1')

    if EDriveSysErr_MCUErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_MCUErr_LEN):
            bit_pos = EDriveSysErr_MCUErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_mcuerr |= (1 << i)
                if debug: print(f'Decode EDriveSysErr_MCUErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_MCUErr_OFFSET, EDriveSysErr_MCUErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_mcuerr |= (1 << (EDriveSysErr_MCUErr_LEN - 1 - i))
                if debug: print(f'Decode EDriveSysErr_MCUErr: byte={byte_i}, bit={bit_i}, val=1')

    if HVSysErr_RelayErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_RelayErr_LEN):
            bit_pos = HVSysErr_RelayErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_relayerr |= (1 << i)
                if debug: print(f'Decode HVSysErr_RelayErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_RelayErr_OFFSET, HVSysErr_RelayErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_relayerr |= (1 << (HVSysErr_RelayErr_LEN - 1 - i))
                if debug: print(f'Decode HVSysErr_RelayErr: byte={byte_i}, bit={bit_i}, val=1')

    if HVSysErr_PackErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_PackErr_LEN):
            bit_pos = HVSysErr_PackErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_packerr |= (1 << i)
                if debug: print(f'Decode HVSysErr_PackErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_PackErr_OFFSET, HVSysErr_PackErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_packerr |= (1 << (HVSysErr_PackErr_LEN - 1 - i))
                if debug: print(f'Decode HVSysErr_PackErr: byte={byte_i}, bit={bit_i}, val=1')

    if HVSysErr_IsolationErr_BYTE_ORDER == 'little_endian':
        for i in range(HVSysErr_IsolationErr_LEN):
            bit_pos = HVSysErr_IsolationErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_isolationerr |= (1 << i)
                if debug: print(f'Decode HVSysErr_IsolationErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(HVSysErr_IsolationErr_OFFSET, HVSysErr_IsolationErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                hvsyserr_isolationerr |= (1 << (HVSysErr_IsolationErr_LEN - 1 - i))
                if debug: print(f'Decode HVSysErr_IsolationErr: byte={byte_i}, bit={bit_i}, val=1')

    if PwrStaErr_BYTE_ORDER == 'little_endian':
        for i in range(PwrStaErr_LEN):
            bit_pos = PwrStaErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                pwrstaerr |= (1 << i)
                if debug: print(f'Decode PwrStaErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(PwrStaErr_OFFSET, PwrStaErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                pwrstaerr |= (1 << (PwrStaErr_LEN - 1 - i))
                if debug: print(f'Decode PwrStaErr: byte={byte_i}, bit={bit_i}, val=1')

    if LVSysErr_PwrOutpErr_BYTE_ORDER == 'little_endian':
        for i in range(LVSysErr_PwrOutpErr_LEN):
            bit_pos = LVSysErr_PwrOutpErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                lvsyserr_pwroutperr |= (1 << i)
                if debug: print(f'Decode LVSysErr_PwrOutpErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LVSysErr_PwrOutpErr_OFFSET, LVSysErr_PwrOutpErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                lvsyserr_pwroutperr |= (1 << (LVSysErr_PwrOutpErr_LEN - 1 - i))
                if debug: print(f'Decode LVSysErr_PwrOutpErr: byte={byte_i}, bit={bit_i}, val=1')

    if EDriveSysErr_ShifterErr_BYTE_ORDER == 'little_endian':
        for i in range(EDriveSysErr_ShifterErr_LEN):
            bit_pos = EDriveSysErr_ShifterErr_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_shiftererr |= (1 << i)
                if debug: print(f'Decode EDriveSysErr_ShifterErr: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(EDriveSysErr_ShifterErr_OFFSET, EDriveSysErr_ShifterErr_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                edrivesyserr_shiftererr |= (1 << (EDriveSysErr_ShifterErr_LEN - 1 - i))
                if debug: print(f'Decode EDriveSysErr_ShifterErr: byte={byte_i}, bit={bit_i}, val=1')

    if FD_EBMErrSta_BYTE_ORDER == 'little_endian':
        for i in range(FD_EBMErrSta_LEN):
            bit_pos = FD_EBMErrSta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fd_ebmerrsta |= (1 << i)
                if debug: print(f'Decode FD_EBMErrSta: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FD_EBMErrSta_OFFSET, FD_EBMErrSta_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fd_ebmerrsta |= (1 << (FD_EBMErrSta_LEN - 1 - i))
                if debug: print(f'Decode FD_EBMErrSta: byte={byte_i}, bit={bit_i}, val=1')

    if LTurnLP_BYTE_ORDER == 'little_endian':
        for i in range(LTurnLP_LEN):
            bit_pos = LTurnLP_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                lturnlp |= (1 << i)
                if debug: print(f'Decode LTurnLP: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(LTurnLP_OFFSET, LTurnLP_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                lturnlp |= (1 << (LTurnLP_LEN - 1 - i))
                if debug: print(f'Decode LTurnLP: byte={byte_i}, bit={bit_i}, val=1')

    if RTurnLP_BYTE_ORDER == 'little_endian':
        for i in range(RTurnLP_LEN):
            bit_pos = RTurnLP_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                rturnlp |= (1 << i)
                if debug: print(f'Decode RTurnLP: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(RTurnLP_OFFSET, RTurnLP_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                rturnlp |= (1 << (RTurnLP_LEN - 1 - i))
                if debug: print(f'Decode RTurnLP: byte={byte_i}, bit={bit_i}, val=1')

    if FDC_VCU_LVStaTooLow_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVStaTooLow_Sta_LEN):
            bit_pos = FDC_VCU_LVStaTooLow_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvstatoolow_sta |= (1 << i)
                if debug: print(f'Decode FDC_VCU_LVStaTooLow_Sta: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVStaTooLow_Sta_OFFSET, FDC_VCU_LVStaTooLow_Sta_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvstatoolow_sta |= (1 << (FDC_VCU_LVStaTooLow_Sta_LEN - 1 - i))
                if debug: print(f'Decode FDC_VCU_LVStaTooLow_Sta: byte={byte_i}, bit={bit_i}, val=1')

    if FDC_VCU_LVStaDropQuick_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVStaDropQuick_Sta_LEN):
            bit_pos = FDC_VCU_LVStaDropQuick_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvstadropquick_sta |= (1 << i)
                if debug: print(f'Decode FDC_VCU_LVStaDropQuick_Sta: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVStaDropQuick_Sta_OFFSET, FDC_VCU_LVStaDropQuick_Sta_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvstadropquick_sta |= (1 << (FDC_VCU_LVStaDropQuick_Sta_LEN - 1 - i))
                if debug: print(f'Decode FDC_VCU_LVStaDropQuick_Sta: byte={byte_i}, bit={bit_i}, val=1')

    if FDC_VCU_LVChrgFreq_Sta_BYTE_ORDER == 'little_endian':
        for i in range(FDC_VCU_LVChrgFreq_Sta_LEN):
            bit_pos = FDC_VCU_LVChrgFreq_Sta_OFFSET + i
            byte_i = bit_pos // 8
            bit_i = bit_pos % 8
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvchrgfreq_sta |= (1 << i)
                if debug: print(f'Decode FDC_VCU_LVChrgFreq_Sta: byte={byte_i}, bit={bit_i}, val=1')
    else:
        for i, (byte_i, bit_i) in enumerate(get_motorola_bit_positions(FDC_VCU_LVChrgFreq_Sta_OFFSET, FDC_VCU_LVChrgFreq_Sta_LEN)):
            if (data[byte_i] >> bit_i) & 1:
                fdc_vcu_lvchrgfreq_sta |= (1 << (FDC_VCU_LVChrgFreq_Sta_LEN - 1 - i))
                if debug: print(f'Decode FDC_VCU_LVChrgFreq_Sta: byte={byte_i}, bit={bit_i}, val=1')

    return canfd_0x117_msg(to_enum(ShiftGearPosnEnum, shiftgearposn, STRICT_ENUM), to_enum(PwrStaEnum, pwrsta, STRICT_ENUM), to_enum(EDriveSysErr_VCUErrEnum, edrivesyserr_vcuerr, STRICT_ENUM), to_enum(EDriveSysErr_AccPedalErrEnum, edrivesyserr_accpedalerr, STRICT_ENUM), meterindspeed_raw32, to_enum(FD_Telltale_FailEnum, fd_telltale_fail, STRICT_ENUM), to_enum(FD_TCS_IndicatorEnum, fd_tcs_indicator, STRICT_ENUM), to_enum(FD_Steering_WarningEnum, fd_steering_warning, STRICT_ENUM), to_enum(FD_ABS_WarningEnum, fd_abs_warning, STRICT_ENUM), to_enum(FD_Battery_Charge_WarningEnum, fd_battery_charge_warning, STRICT_ENUM), to_enum(FD_EDrive_SystemEnum, fd_edrive_system, STRICT_ENUM), to_enum(FD_EPB_ErrorEnum, fd_epb_error, STRICT_ENUM), to_enum(FD_HV_Battery_FaultEnum, fd_hv_battery_fault, STRICT_ENUM), to_enum(FD_Park_Brake_WarningEnum, fd_park_brake_warning, STRICT_ENUM), to_enum(FD_Power_limitationEnum, fd_power_limitation, STRICT_ENUM), to_enum(LimphomeActEnum, limphomeact, STRICT_ENUM), to_enum(EDriveSysErr_MCUErrEnum, edrivesyserr_mcuerr, STRICT_ENUM), to_enum(HVSysErr_RelayErrEnum, hvsyserr_relayerr, STRICT_ENUM), to_enum(HVSysErr_PackErrEnum, hvsyserr_packerr, STRICT_ENUM), to_enum(HVSysErr_IsolationErrEnum, hvsyserr_isolationerr, STRICT_ENUM), to_enum(PwrStaErrEnum, pwrstaerr, STRICT_ENUM), to_enum(LVSysErr_PwrOutpErrEnum, lvsyserr_pwroutperr, STRICT_ENUM), to_enum(EDriveSysErr_ShifterErrEnum, edrivesyserr_shiftererr, STRICT_ENUM), to_enum(FD_EBMErrStaEnum, fd_ebmerrsta, STRICT_ENUM), to_enum(LTurnLPEnum, lturnlp, STRICT_ENUM), to_enum(RTurnLPEnum, rturnlp, STRICT_ENUM), to_enum(FDC_VCU_LVStaTooLow_StaEnum, fdc_vcu_lvstatoolow_sta, STRICT_ENUM), to_enum(FDC_VCU_LVStaDropQuick_StaEnum, fdc_vcu_lvstadropquick_sta, STRICT_ENUM), to_enum(FDC_VCU_LVChrgFreq_StaEnum, fdc_vcu_lvchrgfreq_sta, STRICT_ENUM))

if __name__ == '__main__':
    msg = canfd_0x117_msg(
        ShiftGearPosn=ShiftGearPosnEnum.PARK,  # default: ShiftGearPosnEnum.PARK(0)
        PwrSta=PwrStaEnum.OFF,  # default: PwrStaEnum.OFF(0)
        EDriveSysErr_VCUErr=EDriveSysErr_VCUErrEnum.NORMAL,  # default: EDriveSysErr_VCUErrEnum.NORMAL(0)
        EDriveSysErr_AccPedalErr=EDriveSysErr_AccPedalErrEnum.NORMAL,  # default: EDriveSysErr_AccPedalErrEnum.NORMAL(0)
        MeterIndSpeed_raw32=0,  # default: 0
        FD_Telltale_Fail=FD_Telltale_FailEnum.NORMAL,  # default: FD_Telltale_FailEnum.NORMAL(0)
        FD_TCS_Indicator=FD_TCS_IndicatorEnum.OFF,  # default: FD_TCS_IndicatorEnum.OFF(0)
        FD_Steering_Warning=FD_Steering_WarningEnum.OFF,  # default: FD_Steering_WarningEnum.OFF(0)
        FD_ABS_Warning=FD_ABS_WarningEnum.OFF,  # default: FD_ABS_WarningEnum.OFF(0)
        FD_Battery_Charge_Warning=FD_Battery_Charge_WarningEnum.OFF,  # default: FD_Battery_Charge_WarningEnum.OFF(0)
        FD_EDrive_System=FD_EDrive_SystemEnum.OFF,  # default: FD_EDrive_SystemEnum.OFF(0)
        FD_EPB_Error=FD_EPB_ErrorEnum.OFF,  # default: FD_EPB_ErrorEnum.OFF(0)
        FD_HV_Battery_Fault=FD_HV_Battery_FaultEnum.OFF,  # default: FD_HV_Battery_FaultEnum.OFF(0)
        FD_Park_Brake_Warning=FD_Park_Brake_WarningEnum.OFF,  # default: FD_Park_Brake_WarningEnum.OFF(0)
        FD_Power_limitation=FD_Power_limitationEnum.OFF,  # default: FD_Power_limitationEnum.OFF(0)
        LimphomeAct=LimphomeActEnum.INACTIVE,  # default: LimphomeActEnum.INACTIVE(0)
        EDriveSysErr_MCUErr=EDriveSysErr_MCUErrEnum.NORMAL,  # default: EDriveSysErr_MCUErrEnum.NORMAL(0)
        HVSysErr_RelayErr=HVSysErr_RelayErrEnum.NORMAL,  # default: HVSysErr_RelayErrEnum.NORMAL(0)
        HVSysErr_PackErr=HVSysErr_PackErrEnum.NORMAL,  # default: HVSysErr_PackErrEnum.NORMAL(0)
        HVSysErr_IsolationErr=HVSysErr_IsolationErrEnum.NORMAL,  # default: HVSysErr_IsolationErrEnum.NORMAL(0)
        PwrStaErr=PwrStaErrEnum.NORMAL,  # default: PwrStaErrEnum.NORMAL(0)
        LVSysErr_PwrOutpErr=LVSysErr_PwrOutpErrEnum.NORMAL,  # default: LVSysErr_PwrOutpErrEnum.NORMAL(0)
        EDriveSysErr_ShifterErr=EDriveSysErr_ShifterErrEnum.NORMAL,  # default: EDriveSysErr_ShifterErrEnum.NORMAL(0)
        FD_EBMErrSta=FD_EBMErrStaEnum.OFF,  # default: FD_EBMErrStaEnum.OFF(0)
        LTurnLP=LTurnLPEnum.OFF,  # default: LTurnLPEnum.OFF(0)
        RTurnLP=RTurnLPEnum.OFF,  # default: RTurnLPEnum.OFF(0)
        FDC_VCU_LVStaTooLow_Sta=FDC_VCU_LVStaTooLow_StaEnum.NORMAL,  # default: FDC_VCU_LVStaTooLow_StaEnum.NORMAL(0)
        FDC_VCU_LVStaDropQuick_Sta=FDC_VCU_LVStaDropQuick_StaEnum.NORMAL,  # default: FDC_VCU_LVStaDropQuick_StaEnum.NORMAL(0)
        FDC_VCU_LVChrgFreq_Sta=FDC_VCU_LVChrgFreq_StaEnum.NORMAL,  # default: FDC_VCU_LVChrgFreq_StaEnum.NORMAL(0)
    )
    data_list = generate_0x117_can_msg_bytes(msg)
    print('Generated CAN FD data (list):', data_list)
    data_bytes = bytes(data_list)
    print('Generated CAN FD data (hex):', data_bytes.hex(':'))
    decoded = decode_0x117_can_msg(data_bytes)
    print('Decoded message:', decoded)