using System.CommandLine;
using System.Globalization;
using System.Text;
using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    internal class Program
    {
        static async Task<int> Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;

            var dev_type = new Option<string>("--dev_type")
            {
                Description = "ZLG 裝置型號",
                DefaultValueFactory = parse_result => "ZCAN_USBCANFD_100U",
            };
            var dev_index = new Option<uint>("--dev_index")
            {
                Description = "裝置索引",
                DefaultValueFactory = parse_result => 0
            };
            var can_index = new Option<uint>("--can_index")
            {
                Description = "通道索引",
                DefaultValueFactory = parse_result => 0

            };
            var arb = new Option<uint>("--arb")
            {
                Description = "仲裁位元率 (bps)",
                DefaultValueFactory = parse_result => 104286
            };
            var data = new Option<uint>("--data")
            {
                Description = "資料位元率 (FD data phase, bps)",
                DefaultValueFactory = parse_result => 4260362
            };

            var tx_id = new Option<string>("--txid")
            {
                Description = "UDS TX CAN ID (hex)",
                DefaultValueFactory = parse_result => "682"

            };
            var rx_id = new Option<string>("--rxid")
            {
                Description = "UDS RX CAN ID (hex)",
                DefaultValueFactory = parse_result => "602"
            };

            var did = new Option<string?>("--did")
            {
                Description = "若指定則執行 RDBI，如 1305"
            };

            var clear_dtc = new Option<bool>("--clearDtc")
            {
                Description = "執行 ClearDTC"
            };

            var sniff = new Option<bool>("--sniff")
            {
                Description = "嗅探 (暫不實作)"
            };

            var dump = new Option<string?>("--dump")
            {
                Description = "嗅探輸出檔 (暫不實作)"
            };

            var root = new RootCommand("ZLG / ISO-TP / UDS 工具 (System.CommandLine)");


            // 逐一加入，避免陣列重載不匹配
            root.Options.Add(dev_type);
            root.Options.Add(dev_index);
            root.Options.Add(can_index);
            root.Options.Add(arb);
            root.Options.Add(data);
            root.Options.Add(tx_id);
            root.Options.Add(rx_id);
            root.Options.Add(did);
            root.Options.Add(clear_dtc);
            root.Options.Add(sniff);
            root.Options.Add(dump);

            // === 官方風格：手動 Parse ===
            var result = root.Parse(args);
            if (result.Errors.Count > 0)
            {
                foreach (var e in result.Errors)
                    Console.Error.WriteLine(e.Message);
                return 1;
            }

            root.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                // 這裡用的是 handler 傳進來的 ctx，不再用外面的 result
                string? dt = ctx.GetValue(dev_type);
                var di = ctx.GetValue(dev_index);
                var ci = ctx.GetValue(can_index);
                string? rid_str = ctx.GetValue(rx_id);
                string? tid_str = ctx.GetValue(tx_id);
                uint arb_bps = ctx.GetValue(arb);
                uint dat_bps = ctx.GetValue(data);
                string? didStr = ctx.GetValue(did);
                bool clr = ctx.GetValue(clear_dtc);
                string? dumpStr = ctx.GetValue(dump);

                try
                {
                    uint rid = uint.Parse(rid_str, System.Globalization.NumberStyles.HexNumber);
                    uint tid = uint.Parse(tid_str, System.Globalization.NumberStyles.HexNumber);
                    byte did_high = 0x13;
                    byte did_low = 0x05;
                    DiagnosticSessionType session = DiagnosticSessionType.DefaultSession;
                    await RunCommandAsync(MapDevType(dt), (uint)di, (uint)ci, rid, tid,
                        did_high, did_low,
                        arb_bps, dat_bps, session, ct);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
                return 0;
            }
            );

            return await root.Parse(args).InvokeAsync();
        }

        private static async Task<int> RunCommandAsync(uint device_type,
            uint dev_idx,
            uint chn_idx,
            uint rx_id,
            uint tx_id,
            byte did_high,
            byte did_low,
            uint abit_timing,
            uint dbit_timing,
            DiagnosticSessionType session_type = DiagnosticSessionType.DefaultSession,
            CancellationToken ct = default)
        {
            using ICanTransport can = new ZlgCanTransport(
                  devType: device_type,
                  devIndex: dev_idx,
                  canIndex: chn_idx,
                  arbBtr: abit_timing, dataBtr: dbit_timing
             );

            var iso = new IsoTpClient(can, txId: tx_id, rxId: rx_id);
            var uds = new UdsClient(iso);

            if (session_type != DiagnosticSessionType.DefaultSession)
                await uds.ChangeSessionAsync(DiagnosticSessionType.ExtendedSession,
                    new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true));

            Console.WriteLine($"Read DID {did_high.ToString("X2")}{did_low.ToString("X2")}");
            var resp = await uds.ReadDidAsync(did_high, did_low,
                new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true));
            Console.WriteLine("Resp: " + BitConverter.ToString(resp));


            Console.WriteLine("Clear DTC");
            bool cleared = await uds.ClearDtcAsync(new UdsRequestOptions(TimeoutMs: 5000));
            Console.WriteLine("Cleared: " + cleared);
            return 0;
        }

        private static uint ParseHex32(string s)
        {
            if (s.StartsWith("0x", StringComparison.OrdinalIgnoreCase)) s = s[2..];
            return uint.Parse(s, NumberStyles.AllowHexSpecifier);
        }

        private static uint MapDevType(string s)
        {
            // 依你的 ZLGAPI.cs 常數調整
            return s.ToUpperInvariant() switch
            {
                "ZCAN_USBCANFD_100U" => ZLGAPI.ZLGCAN.ZCAN_USBCANFD_100U,
                _ => throw new ArgumentOutOfRangeException(nameof(s), $"Unknown devType: {s}")
            };
        }
    }
}