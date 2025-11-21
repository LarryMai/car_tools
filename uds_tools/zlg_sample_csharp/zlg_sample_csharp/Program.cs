using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    internal class Program
    {
        static async Task Main(string[] args) 
        {
            // ZLG CANFD 示例
            uint device_type = ZLGAPI.ZLGCAN.ZCAN_USBCANFD_100U;
            uint dev_idx = 0;
            uint chn_idx = 0;
            uint abit_timing = 104286; 
            uint dbit_timing = 4260362; //500k
            // 注意：請把 zlgcan.dll 放到可執行檔同資料夾
            using ICanTransport can = new ZlgCanTransport(
                devType: device_type,
                devIndex: dev_idx, 
                canIndex: chn_idx,
                arbBtr: abit_timing, dataBtr: dbit_timing
           );

            var iso = new IsoTpClient(can, txId: 0x682, rxId: 0x602);
            var uds = new UdsClient(iso);
            await uds.ChangeSessionAsync(DiagnosticSessionType.ExtendedSession, 
                new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true)); 

            Console.WriteLine("Read DID 1305");
            var resp = await uds.ReadDidAsync( 0x13, 0x05, 
                new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true));
            Console.WriteLine("Resp: " + BitConverter.ToString(resp));

            Console.WriteLine("Clear DTC");
            bool cleared = await uds.ClearDtcAsync(new UdsRequestOptions(TimeoutMs: 5000));
            Console.WriteLine("Cleared: " + cleared);
        }
    }
}
