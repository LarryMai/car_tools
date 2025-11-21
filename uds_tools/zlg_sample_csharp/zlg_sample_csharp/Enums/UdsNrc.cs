using System;

namespace zlg_sample_csharp.Enums
{
    /// <summary>UDS 常見負回應碼（NRC: Negative Response Code）</summary>
    public enum UdsNrc : byte
    {
        GeneralReject = 0x10,
        ServiceNotSupported = 0x11,
        SubFunctionNotSupported = 0x12,
        IncorrectMessageLength = 0x13,
        BusyRepeatRequest = 0x21,
        ConditionsNotCorrect = 0x22,
        RequestSequenceError = 0x24,
        RequestOutOfRange = 0x31,
        SecurityAccessDenied = 0x33,
        InvalidKey = 0x35,
        ExceededNumberOfAttempts = 0x36,
        RequiredTimeDelayNotExpired = 0x37,
        ResponsePending = 0x78,
        SubFunctionNotSupportedInActiveSession = 0x7E,
        ServiceNotSupportedInActiveSession = 0x7F,
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

        public static string AsString(this UdsNrc n) => n switch
        {
            // more common NRCs
            (UdsNrc)0x10 => "GeneralReject (0x10)",
            UdsNrc.ServiceNotSupported => "ServiceNotSupported (0x11)",
            UdsNrc.SubFunctionNotSupported => "SubFunctionNotSupported (0x12)",
            UdsNrc.IncorrectMessageLength => "IncorrectMessageLength (0x13)",
            (UdsNrc)0x21 => "BusyRepeatRequest (0x21)",
            UdsNrc.ConditionsNotCorrect => "ConditionsNotCorrect (0x22)",
            UdsNrc.RequestSequenceError => "RequestSequenceError (0x24)",
            UdsNrc.RequestOutOfRange => "RequestOutOfRange (0x31)",
            UdsNrc.SecurityAccessDenied => "SecurityAccessDenied (0x33)",
            (UdsNrc)0x35 => "InvalidKey (0x35)",
            (UdsNrc)0x36 => "ExceededNumberOfAttempts (0x36)",
            (UdsNrc)0x37 => "RequiredTimeDelayNotExpired (0x37)",
            UdsNrc.ResponsePending => "ResponsePending (0x78)",
            (UdsNrc)0x7E => "SubFunctionNotSupportedInActiveSession (0x7E)",
            (UdsNrc)0x7F => "ServiceNotSupportedInActiveSession (0x7F)",
            _ => $"Unknown NRC (0x{(byte)n:X2})"
        };

        // 小工具：若 enum 未涵蓋，仍可穩定輸出
        public static string AsString(byte nrcRaw)
            => ((UdsNrc)nrcRaw).AsString();
    }
}
