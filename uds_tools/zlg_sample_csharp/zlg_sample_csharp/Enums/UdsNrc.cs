using System;

namespace zlg_sample_csharp.Enums
{
    /// <summary>UDS 常見負回應碼（NRC: Negative Response Code）</summary>
    /// <summary>UDS Negative Response Codes (NRC) - expanded set from ISO 14229-1</summary>
    public enum UdsNrc : byte
    {
        // Core / generic
        GeneralReject = 0x10,
        ServiceNotSupported = 0x11,
        SubFunctionNotSupported = 0x12,
        IncorrectMessageLengthOrInvalidFormat = 0x13,
        ResponseTooLong = 0x14,

        // Flow / state
        BusyRepeatRequest = 0x21,
        ConditionsNotCorrect = 0x22,
        RequestSequenceError = 0x24,
        NoResponseFromSubnetComponent = 0x25, // vendor usage varies
        FailurePreventsExecutionOfRequestedAction = 0x26,

        // Range / security
        RequestOutOfRange = 0x31,
        SecurityAccessDenied = 0x33,
        InvalidKey = 0x35,
        ExceededNumberOfAttempts = 0x36,
        RequiredTimeDelayNotExpired = 0x37,

        // Download/Upload / programming
        UploadDownloadNotAccepted = 0x70,
        TransferDataSuspended = 0x71,
        GeneralProgrammingFailure = 0x72,
        WrongBlockSequenceCounter = 0x73,

        // Processing
        RequestCorrectlyReceivedResponsePending = 0x78, // "ResponsePending"

        // Session/Service availability
        SubFunctionNotSupportedInActiveSession = 0x7E,
        ServiceNotSupportedInActiveSession = 0x7F,

        // Environmental / precondition (commonly used set)
        RpmTooHigh = 0x81,
        RpmTooLow = 0x82,
        EngineIsRunning = 0x83,
        EngineIsNotRunning = 0x84,
        EngineRunTimeTooLow = 0x85,
        TemperatureTooHigh = 0x86,
        TemperatureTooLow = 0x87,
        VehicleSpeedTooHigh = 0x88,
        VehicleSpeedTooLow = 0x89,
        ThrottlePedalTooHigh = 0x8A,
        ThrottlePedalTooLow = 0x8B,
        TransmissionRangeNotInNeutral = 0x8C,
        TransmissionRangeNotInGear = 0x8D,
        BrakeSwitchNotClosed = 0x8F,
        ShifterLeverNotInPark = 0x90,
        TorqueConverterClutchLocked = 0x91,
        VoltageTooHigh = 0x92,
        VoltageTooLow = 0x93
    }

    public static class UdsNrcExtensions
    {
        /// <summary>回應是否為指定服務的正回應（正回應 SID = 請求 SID + 0x40）</summary>
        public static bool IsPositive(byte requestSid, ReadOnlySpan<byte> resp)
            => resp.Length > 0 && resp[0] == (byte)(requestSid + 0x40);

        /// <summary>嘗試解析負回應碼（格式：7F [reqSid] [NRC]）</summary>
        public static bool TryParseNrc(ReadOnlySpan<byte> resp, out UdsNrc nrc, out byte requestSid)
        {
            if (resp.Length >= 3 && resp[0] == 0x7F)
            {
                requestSid = resp[1];
                nrc = (UdsNrc)resp[2];
                return true;
            }
            requestSid = 0;
            nrc = default;
            return false;
        }


        /// <summary>Human-friendly description (English + hex)</summary>
        public static string AsString(this UdsNrc n) => n switch
        {
            UdsNrc.GeneralReject => "GeneralReject (0x10)",
            UdsNrc.ServiceNotSupported => "ServiceNotSupported (0x11)",
            UdsNrc.SubFunctionNotSupported => "SubFunctionNotSupported (0x12)",
            UdsNrc.IncorrectMessageLengthOrInvalidFormat => "IncorrectMessageLengthOrInvalidFormat (0x13)",
            UdsNrc.ResponseTooLong => "ResponseTooLong (0x14)",
            UdsNrc.BusyRepeatRequest => "BusyRepeatRequest (0x21)",
            UdsNrc.ConditionsNotCorrect => "ConditionsNotCorrect (0x22)",
            UdsNrc.RequestSequenceError => "RequestSequenceError (0x24)",
            UdsNrc.NoResponseFromSubnetComponent => "NoResponseFromSubnetComponent (0x25)",
            UdsNrc.FailurePreventsExecutionOfRequestedAction => "FailurePreventsExecutionOfRequestedAction (0x26)",
            UdsNrc.RequestOutOfRange => "RequestOutOfRange (0x31)",
            UdsNrc.SecurityAccessDenied => "SecurityAccessDenied (0x33)",
            UdsNrc.InvalidKey => "InvalidKey (0x35)",
            UdsNrc.ExceededNumberOfAttempts => "ExceededNumberOfAttempts (0x36)",
            UdsNrc.RequiredTimeDelayNotExpired => "RequiredTimeDelayNotExpired (0x37)",
            UdsNrc.UploadDownloadNotAccepted => "UploadDownloadNotAccepted (0x70)",
            UdsNrc.TransferDataSuspended => "TransferDataSuspended (0x71)",
            UdsNrc.GeneralProgrammingFailure => "GeneralProgrammingFailure (0x72)",
            UdsNrc.WrongBlockSequenceCounter => "WrongBlockSequenceCounter (0x73)",
            UdsNrc.RequestCorrectlyReceivedResponsePending => "ResponsePending (0x78)",
            UdsNrc.SubFunctionNotSupportedInActiveSession => "SubFunctionNotSupportedInActiveSession (0x7E)",
            UdsNrc.ServiceNotSupportedInActiveSession => "ServiceNotSupportedInActiveSession (0x7F)",
            UdsNrc.RpmTooHigh => "RpmTooHigh (0x81)",
            UdsNrc.RpmTooLow => "RpmTooLow (0x82)",
            UdsNrc.EngineIsRunning => "EngineIsRunning (0x83)",
            UdsNrc.EngineIsNotRunning => "EngineIsNotRunning (0x84)",
            UdsNrc.EngineRunTimeTooLow => "EngineRunTimeTooLow (0x85)",
            UdsNrc.TemperatureTooHigh => "TemperatureTooHigh (0x86)",
            UdsNrc.TemperatureTooLow => "TemperatureTooLow (0x87)",
            UdsNrc.VehicleSpeedTooHigh => "VehicleSpeedTooHigh (0x88)",
            UdsNrc.VehicleSpeedTooLow => "VehicleSpeedTooLow (0x89)",
            UdsNrc.ThrottlePedalTooHigh => "ThrottlePedalTooHigh (0x8A)",
            UdsNrc.ThrottlePedalTooLow => "ThrottlePedalTooLow (0x8B)",
            UdsNrc.TransmissionRangeNotInNeutral => "TransmissionRangeNotInNeutral (0x8C)",
            UdsNrc.TransmissionRangeNotInGear => "TransmissionRangeNotInGear (0x8D)",
            UdsNrc.BrakeSwitchNotClosed => "BrakeSwitchNotClosed (0x8F)",
            UdsNrc.ShifterLeverNotInPark => "ShifterLeverNotInPark (0x90)",
            UdsNrc.TorqueConverterClutchLocked => "TorqueConverterClutchLocked (0x91)",
            UdsNrc.VoltageTooHigh => "VoltageTooHigh (0x92)",
            UdsNrc.VoltageTooLow => "VoltageTooLow (0x93)",
            _ => $"Unknown NRC (0x{((byte)n):X2})"
        };

        // 小工具：若 enum 未涵蓋，仍可穩定輸出
        public static string AsString(byte nrcRaw)
            => ((UdsNrc)nrcRaw).AsString();
    }
}
