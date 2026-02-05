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
    }
}
