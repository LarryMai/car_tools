using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    public static class UdsHelpers
    {
        /// <summary>正回應判斷（正回應 SID = 請求 SID + 0x40）</summary>
        public static bool IsPositive(byte requestSid, ReadOnlySpan<byte> resp)
            => resp.Length > 0 && resp[0] == (byte)(requestSid + 0x40);

        /// <summary>解析負回應碼（格式：7F [reqSid] [NRC]）</summary>
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

        /// <summary>轉成可讀字串（英文＋Hex）</summary>
        public static string AsString(this UdsNrc n) => n switch
        {
            UdsNrc.GeneralReject => "GeneralReject (0x10)",
            UdsNrc.ServiceNotSupported => "ServiceNotSupported (0x11)",
            UdsNrc.SubFunctionNotSupported => "SubFunctionNotSupported (0x12)",
            UdsNrc.IncorrectMessageLength => "IncorrectMessageLength (0x13)",
            UdsNrc.BusyRepeatRequest => "BusyRepeatRequest (0x21)",
            UdsNrc.ConditionsNotCorrect => "ConditionsNotCorrect (0x22)",
            UdsNrc.RequestSequenceError => "RequestSequenceError (0x24)",
            UdsNrc.RequestOutOfRange => "RequestOutOfRange (0x31)",
            UdsNrc.SecurityAccessDenied => "SecurityAccessDenied (0x33)",
            UdsNrc.InvalidKey => "InvalidKey (0x35)",
            UdsNrc.ExceededNumberOfAttempts => "ExceededNumberOfAttempts (0x36)",
            UdsNrc.RequiredTimeDelayNotExpired => "RequiredTimeDelayNotExpired (0x37)",
            UdsNrc.ResponsePending => "ResponsePending (0x78)",
            UdsNrc.SubFunctionNotSupportedInActiveSession => "SubFunctionNotSupportedInActiveSession (0x7E)",
            UdsNrc.ServiceNotSupportedInActiveSession => "ServiceNotSupportedInActiveSession (0x7F)",
            _ => $"Unknown NRC (0x{((byte)n):X2})"
        };
    }
}
