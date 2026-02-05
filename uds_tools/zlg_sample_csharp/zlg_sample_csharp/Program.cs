using System.CommandLine;
using System.CommandLine.Parsing;
using System.Diagnostics;
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
            var config = AppConfig.Load();

            // Define options with defaults from AppConfig
            var dev_type = new Option<string>("--dev_type") { Description = "ZLG 裝置型號", DefaultValueFactory = _ => config.DeviceType };
            var dev_index = new Option<uint>("--dev_index") { Description = "裝置索引", DefaultValueFactory = _ => config.DeviceIndex };
            var can_index = new Option<uint>("--can_index") { Description = "通道索引", DefaultValueFactory = _ => config.ChannelIndex };
            var arb = new Option<uint>("--arb") { Description = "仲裁位元率 (bps)", DefaultValueFactory = _ => config.ArbBps };
            var data = new Option<uint>("--data") { Description = "資料位元率 (FD data phase, bps)", DefaultValueFactory = _ => config.DataBps };
            var tx_id = new Option<string>("--txid") { Description = "UDS TX CAN ID (hex)", DefaultValueFactory = _ => config.TxId };
            var rx_id = new Option<string>("--rxid") { Description = "UDS RX CAN ID (hex)", DefaultValueFactory = _ => config.RxId };
            
            // Action parameter
            var action = new Option<UDSCommandType>("--action") 
            { 
                Description = "執行動作 (sniffer, flash)", 
                DefaultValueFactory = _ => config.CommandType 
            };

            // Sniffer specific options
            var did = new Option<string?>("--did") { Description = "若指定則執行 RDBI，如 1305" };
            var clear_dtc = new Option<bool>("--clearDtc") { Description = "執行 ClearDTC" };
            var new_window = new Option<bool>("--new-window") { Description = "在新視窗顯示監聽內容", DefaultValueFactory = _ => config.SnifferInNewWindow };
            
            // Flash specific options
            var hex_dir = new Option<string>("--hex_dir") { Description = "HEX 檔案目錄", DefaultValueFactory = _ => config.HexDir };

            // Root command
            var root = new RootCommand("ZLG / ISO-TP / UDS 工具 (System.CommandLine)");
            
            // Add options to root
            root.Options.Add(action);
            root.Options.Add(dev_type);
            root.Options.Add(dev_index);
            root.Options.Add(can_index);
            root.Options.Add(arb);
            root.Options.Add(data);
            root.Options.Add(tx_id);
            root.Options.Add(rx_id);
            root.Options.Add(did);
            root.Options.Add(clear_dtc);
            root.Options.Add(new_window);
            root.Options.Add(hex_dir);

            // Set root handler to dispatch based on 'action'
            root.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                UDSCommandType act = ctx.GetValue(action);
                string dt = ctx.GetValue(dev_type)!;
                uint di = ctx.GetValue(dev_index);
                uint ci = ctx.GetValue(can_index);
                uint rid = uint.Parse(ctx.GetValue(rx_id)!, NumberStyles.HexNumber);
                uint tid = uint.Parse(ctx.GetValue(tx_id)!, NumberStyles.HexNumber);
                uint arb_bps = ctx.GetValue(arb);
                uint dat_bps = ctx.GetValue(data);
                
                if (act == UDSCommandType.COMMAND_UDS_FLASH)
                {
                    string? hexDir = ctx.GetValue(hex_dir);
                    if (string.IsNullOrEmpty(hexDir))
                    {
                        Console.WriteLine("Error: --hex_dir is required for flash action.");
                        return;
                    }
                    await RunFlashCommandAsync(MapDevType(dt), di, ci, rid, tid, arb_bps, dat_bps, hexDir, ct);
                }
                else if (act == UDSCommandType.COMMAND_SNIFFER)
                {
                    string? didStr = ctx.GetValue(did);
                    bool clr = ctx.GetValue(clear_dtc);
                    bool nw = ctx.GetValue(new_window);
                    await RunSnifferCommandAsync(MapDevType(dt), di, ci, rid, tid, arb_bps, dat_bps, didStr, clr, config.Commands, nw, config.SnifferLogFile, ct);
                }
                else
                {
                    Console.WriteLine($"Unknown or unspecified action: {act}. Defaulting to Sniffer if not 0.");
                    if (act != UDSCommandType.COMMAND_UNKNOWN)
                    {
                         string? didStr = ctx.GetValue(did);
                         bool clr = ctx.GetValue(clear_dtc);
                         bool nw = ctx.GetValue(new_window);
                         await RunSnifferCommandAsync(MapDevType(dt), di, ci, rid, tid, arb_bps, dat_bps, didStr, clr, config.Commands, nw, config.SnifferLogFile, ct);
                    }
                }
            });

            // Keep 'flash' subcommand as alias
            var flashCommand = new Command("flash", "執行 UDS Flashing 流程 (Alias for --action flash)");
            flashCommand.Options.Add(dev_type);
            flashCommand.Options.Add(dev_index);
            flashCommand.Options.Add(can_index);
            flashCommand.Options.Add(arb);
            flashCommand.Options.Add(data);
            flashCommand.Options.Add(tx_id);
            flashCommand.Options.Add(rx_id);
            flashCommand.Options.Add(hex_dir);

            flashCommand.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                string dt = ctx.GetValue(dev_type)!;
                uint di = ctx.GetValue(dev_index);
                uint ci = ctx.GetValue(can_index);
                uint rid = uint.Parse(ctx.GetValue(rx_id)!, NumberStyles.HexNumber);
                uint tid = uint.Parse(ctx.GetValue(tx_id)!, NumberStyles.HexNumber);
                uint arb_bps = ctx.GetValue(arb);
                uint dat_bps = ctx.GetValue(data);
                string? hexDir = ctx.GetValue(hex_dir);

                if (string.IsNullOrEmpty(hexDir))
                {
                    Console.WriteLine("Error: --hex_dir is required for flash command.");
                    return;
                }
                await RunFlashCommandAsync(MapDevType(dt), di, ci, rid, tid, arb_bps, dat_bps, hexDir, ct);
            });

            // Add sniffer subcommand explicitly if user wants to use "sniffer" keyword
            var snifferCommand = new Command("sniffer", "CAN 監聽模式 (可選 UDS 功能)");
            snifferCommand.Options.Add(dev_type);
            snifferCommand.Options.Add(dev_index);
            snifferCommand.Options.Add(can_index);
            snifferCommand.Options.Add(arb);
            snifferCommand.Options.Add(data);
            snifferCommand.Options.Add(tx_id);
            snifferCommand.Options.Add(rx_id);
            snifferCommand.Options.Add(did);
            snifferCommand.Options.Add(clear_dtc);
            snifferCommand.Options.Add(new_window);
            
            snifferCommand.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                string dt = ctx.GetValue(dev_type)!;
                uint di = ctx.GetValue(dev_index);
                uint ci = ctx.GetValue(can_index);
                uint rid = uint.Parse(ctx.GetValue(rx_id)!, NumberStyles.HexNumber);
                uint tid = uint.Parse(ctx.GetValue(tx_id)!, NumberStyles.HexNumber);
                uint arb_bps = ctx.GetValue(arb);
                uint dat_bps = ctx.GetValue(data);
                string? didStr = ctx.GetValue(did);
                bool clr = ctx.GetValue(clear_dtc);
                bool nw = ctx.GetValue(new_window);

                await RunSnifferCommandAsync(MapDevType(dt), di, ci, rid, tid, arb_bps, dat_bps, didStr, clr, config.Commands, nw, config.SnifferLogFile, ct);
            });

            root.Add(flashCommand);
            root.Add(snifferCommand);

            return await root.Parse(args).InvokeAsync();
        }

        private static async Task RunSnifferCommandAsync(uint device_type, uint dev_idx, uint chn_idx, uint rx_id, uint tx_id, uint abit_timing, uint dbit_timing, string? didStr, bool clearDtc, List<UdsCommandConfig>? commands, bool newWindow, string logFile, CancellationToken ct)
        {
            using ICanTransport can = new ZlgCanTransport(device_type, dev_idx, chn_idx, abit_timing, dbit_timing);
            var iso = new IsoTpClient(can, txId: tx_id, rxId: rx_id);
            var uds = new UdsClient(iso);

            bool actionTaken = false;

            // 1. CLI Args (Highest priority or processed first)
            if (!string.IsNullOrEmpty(didStr))
            {
                actionTaken = true;
                byte did_h = byte.Parse(didStr.Substring(0, 2), NumberStyles.HexNumber);
                byte did_l = byte.Parse(didStr.Substring(2, 2), NumberStyles.HexNumber);
                Console.WriteLine($"[Active] Read DID {didStr}");
                var resp = await uds.ReadDidAsync(did_h, did_l, new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true, CancellationToken: ct));
                Console.WriteLine("Resp: " + BitConverter.ToString(resp));
            }

            if (clearDtc)
            {
                actionTaken = true;
                Console.WriteLine("[Active] Clear DTC");
                bool cleared = await uds.ClearDtcAsync(new UdsRequestOptions(TimeoutMs: 5000, CancellationToken: ct));
                Console.WriteLine("Cleared: " + cleared);
            }

            // 2. Configured Commands
            if (commands != null)
            {
                foreach (var cmd in commands)
                {
                    if (cmd.Type.ToLower() == "one_shot" || string.IsNullOrEmpty(cmd.Type))
                    {
                        if (cmd.Service == "0x22" && !string.IsNullOrEmpty(cmd.Did))
                        {
                            actionTaken = true;
                            string d = cmd.Did.Replace("0x", "").Replace(" ", "");
                            if (d.Length == 4)
                            {
                                byte did_h = byte.Parse(d.Substring(0, 2), NumberStyles.HexNumber);
                                byte did_l = byte.Parse(d.Substring(2, 2), NumberStyles.HexNumber);
                                Console.WriteLine($"[Active Config] Read DID {cmd.Did}");
                                var resp = await uds.ReadDidAsync(did_h, did_l, new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true, CancellationToken: ct));
                                Console.WriteLine("Resp: " + BitConverter.ToString(resp));
                            }
                        }
                    }
                    else if (cmd.Type.ToLower() == "periodically")
                    {
                        Console.WriteLine($"[Active Config] Skipping periodic command: {cmd.Service} {cmd.Did} (Not implemented)");
                    }
                }
            }

            // 3. Passive Sniffer
            
            StreamWriter? logWriter = null;
            if (newWindow)
            {
                // Clear log file
                try 
                {
                    File.WriteAllText(logFile, string.Empty);
                    logWriter = new StreamWriter(logFile, append: true, Encoding.UTF8) { AutoFlush = true };
                    
                    Console.WriteLine($"[Passive] Sniffer mode output redirected to {logFile}");
                    Console.WriteLine("[Passive] Opening new window to tail log...");
                    
                    // Spawn new window with PowerShell Get-Content -Wait
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = "cmd",
                        Arguments = $"/c start \"ZLG Sniffer Monitor\" powershell -NoExit -Command \"Get-Content '{logFile}' -Wait\"",
                        UseShellExecute = false,
                        CreateNoWindow = true 
                    });
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error preparing new window/log: {ex.Message}");
                    newWindow = false; // Fallback to console
                }
            }
            
            if (!newWindow)
            {
                Console.WriteLine("[Passive] Sniffer mode started. Press Ctrl+C to stop.");
                Console.WriteLine("ID\tDLC\tData");
                Console.WriteLine("--------------------------------------------------");
            }
            
            while (!ct.IsCancellationRequested)
            {
                try 
                {
                    // Receive any frame (expectedCanId = null)
                    var (id, data) = await can.ReceiveAsync(null, 100, ct);
                    string msg = $"{id:X3}\t{data.Length}\t{BitConverter.ToString(data)}";
                    
                    if (newWindow && logWriter != null)
                    {
                        await logWriter.WriteLineAsync(msg);
                    }
                    else
                    {
                        Console.WriteLine(msg);
                    }
                }
                catch (TimeoutException)
                {
                    // Timeout is normal in sniffer mode, just continue
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("\nStopped.");
                    break;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error receiving: {ex.Message}");
                }
            }
            
            logWriter?.Dispose();
        }

        private static async Task RunFlashCommandAsync(uint device_type, uint dev_idx, uint chn_idx, uint rx_id, uint tx_id, uint abit_timing, uint dbit_timing, string hexDir, CancellationToken ct)
        {
            using ICanTransport can = new ZlgCanTransport(device_type, dev_idx, chn_idx, abit_timing, dbit_timing);
            var iso = new IsoTpClient(can, txId: tx_id, rxId: rx_id);
            var uds = new UdsClient(iso);
            var flashManager = new FlashManager(uds);

            await flashManager.FlashAsync(hexDir, ct);
        }

        private static uint MapDevType(string s)
        {
            return s.ToUpperInvariant() switch
            {
                "ZCAN_USBCANFD_100U" => ZLGAPI.ZLGCAN.ZCAN_USBCANFD_100U,
                _ => throw new ArgumentOutOfRangeException(nameof(s), $"Unknown devType: {s}")
            };
        }
    }
}
