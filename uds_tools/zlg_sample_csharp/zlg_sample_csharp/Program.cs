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

            // 1. Define GLOBAL options (Hardware/Transport settings)
            var dev_type = new Option<string>("--dev_type") { Description = "ZLG 裝置型號", DefaultValueFactory = _ => config.DeviceType };
            var dev_index = new Option<uint>("--dev_index") { Description = "裝置索引", DefaultValueFactory = _ => config.DeviceIndex };
            var can_index = new Option<uint>("--can_index") { Description = "通道索引", DefaultValueFactory = _ => config.ChannelIndex };
            var arb = new Option<uint>("--arb") { Description = "仲裁位元率 (bps)", DefaultValueFactory = _ => config.ArbBps };
            var data = new Option<uint>("--data") { Description = "資料位元率 (FD data phase, bps)", DefaultValueFactory = _ => config.DataBps };
            var tx_id = new Option<string>("--txid") { Description = "UDS TX CAN ID (hex)", DefaultValueFactory = _ => config.TxId };
            var rx_id = new Option<string>("--rxid") { Description = "UDS RX CAN ID (hex)", DefaultValueFactory = _ => config.RxId };

            // 2. Define LOCAL options (Command specific)
            var action = new Option<UDSCommandType>("--action") { Description = "執行動作 (sniffer, flash)", DefaultValueFactory = _ => config.CommandType };
            var did = new Option<string?>("--did") { Description = "若指定則執行 RDBI，如 1305" };
            var clear_dtc = new Option<bool>("--clearDtc") { Description = "執行 ClearDTC" };
            var new_window = new Option<bool>("--new-window") { Description = "在新視窗顯示監聽內容", DefaultValueFactory = _ => config.Sniffer.SnifferInNewWindow };
            var hex_dir = new Option<string>("--hex_dir") { Description = "HEX 檔案目錄", DefaultValueFactory = _ => config.HexDir };
            var bin_file = new Option<string>("--bin") { Description = "輸入 Binary 檔案路徑" };
            var base_addr = new Option<string>("--addr") { Description = "起始位址 (hex), e.g. 0x10000", DefaultValueFactory = _ => "0x0" };
            var out_dir = new Option<string?>("--out_dir") { Description = "輸出目錄 (選填)" };
            var gen_zflash = new Option<bool>("--gen_zflash") { Description = "是否生成 .zflash 設定檔", DefaultValueFactory = _ => true };
            var log_output = new Option<string?>("--log") { Description = "輸出 Log 檔案路徑 (選填，若未指定則不記錄)" };
            var verbose = new Option<bool>("--verbose") { Description = "顯示詳細傳輸資料 (Raw Data)", DefaultValueFactory = _ => false };

            var root = new RootCommand("ZLG / ISO-TP / UDS 工具 (System.CommandLine)");
            root.Options.Add(dev_type);
            root.Options.Add(dev_index);
            root.Options.Add(can_index);
            root.Options.Add(arb);
            root.Options.Add(data);
            root.Options.Add(tx_id);
            root.Options.Add(rx_id);
            root.Options.Add(action);
            root.Options.Add(hex_dir);
            root.Options.Add(log_output);
            root.Options.Add(verbose);

            // --- Root Command Logic ---
            root.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                using var logger = SetupLogging(ctx.GetValue(log_output));
                var p = GetCommonParams(ctx, dev_type, dev_index, can_index, tx_id, rx_id, arb, data);
                UDSCommandType act = ctx.GetValue(action);
                
                switch (act)
                {
                    case UDSCommandType.COMMAND_UDS_FLASH:
                        string? hdir = ctx.GetValue(hex_dir);
                        if (string.IsNullOrEmpty(hdir))
                        {
                            Console.WriteLine("Error: --hex_dir is required for flash action.");
                            return;
                        }
                        await RunFlashCommandAsync(p.dt, p.di, p.ci, p.rid, p.tid, p.arb, p.dat, hdir, config.Flash, ctx.GetValue(verbose), ct);
                        break;

                    case UDSCommandType.COMMAND_SNIFFER:
                    default:
                        // Default to sniffer if unknown or specified as sniffer
                        await RunSnifferWithArgsAsync(ctx, p.dt, p.di, p.ci, p.rid, p.tid, p.arb, p.dat, config, did, clear_dtc, new_window, ct);
                        break;
                }
            });

            // --- Subcommands ---

            var flashCommand = new Command("flash", "執行 UDS Flashing 流程");
            flashCommand.Options.Add(dev_type);
            flashCommand.Options.Add(dev_index);
            flashCommand.Options.Add(can_index);
            flashCommand.Options.Add(arb);
            flashCommand.Options.Add(data);
            flashCommand.Options.Add(tx_id);
            flashCommand.Options.Add(rx_id);
            flashCommand.Options.Add(hex_dir);
            flashCommand.Options.Add(log_output);
            flashCommand.Options.Add(verbose);
            flashCommand.SetAction(async (ParseResult ctx, CancellationToken ct) =>
            {
                using var logger = SetupLogging(ctx.GetValue(log_output));
                var p = GetCommonParams(ctx, dev_type, dev_index, can_index, tx_id, rx_id, arb, data);
                string? hdir = ctx.GetValue(hex_dir);
                bool verb = ctx.GetValue(verbose);
                if (string.IsNullOrEmpty(hdir)) { Console.WriteLine("Error: --hex_dir is required."); return; }
                await RunFlashCommandAsync(p.dt, p.di, p.ci, p.rid, p.tid, p.arb, p.dat, hdir, config.Flash, verb, ct);
            });

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
                var p = GetCommonParams(ctx, dev_type, dev_index, can_index, tx_id, rx_id, arb, data);
                await RunSnifferWithArgsAsync(ctx, p.dt, p.di, p.ci, p.rid, p.tid, p.arb, p.dat, config, did, clear_dtc, new_window, ct);
            });

            var convertCommand = new Command("convert", "將 Bin 轉換為 Hex 並產生 .zflash");
            convertCommand.Options.Add(tx_id); // Convert also uses IDs for ZFlash
            convertCommand.Options.Add(rx_id);
            convertCommand.Options.Add(bin_file);
            convertCommand.Options.Add(base_addr);
            convertCommand.Options.Add(out_dir);
            convertCommand.Options.Add(gen_zflash);
            convertCommand.SetAction((ParseResult ctx) =>
            {
                string? bin = ctx.GetValue(bin_file);
                if (string.IsNullOrEmpty(bin) || !File.Exists(bin)) { Console.WriteLine("Error: Valid --bin file is required."); return; }

                string addrStr = ctx.GetValue(base_addr)!.Replace("0x", "");
                uint addr = uint.Parse(addrStr, NumberStyles.HexNumber);
                string odir = ctx.GetValue(out_dir) ?? Path.GetDirectoryName(Path.GetFullPath(bin))!;
                if (!Directory.Exists(odir)) Directory.CreateDirectory(odir);

                string hpath = Path.Combine(odir, $"addr_{addr:X6}_{Path.GetFileNameWithoutExtension(bin)}.hex");
                Console.WriteLine($"Converting {bin} to {hpath} at address 0x{addr:X}...");
                BinToHexConverter.Convert(bin, hpath, addr);

                if (ctx.GetValue(gen_zflash))
                {
                    string zf = Path.Combine(odir, $"{Path.GetFileNameWithoutExtension(bin)}.zflash");
                    ZFlashGenerator.Generate(zf, new[] { hpath }, ctx.GetValue(tx_id)!, ctx.GetValue(rx_id)!);
                    Console.WriteLine($"ZFlash generated: {zf}");
                }
            });

            // Batch Convert subcommand
            var bat_file = new Option<string?>("--bat") { Description = "輸入 .bat 腳本路徑" };
            var src_dir = new Option<string?>("--src_dir") { Description = "輸入來源目錄 (若不使用 .bat)" };

            var batchConvertCommand = new Command("batch-convert", "批量將 Bin/Rle 轉換為 Hex 並產生 .zflash");
            batchConvertCommand.Options.Add(bat_file);
            batchConvertCommand.Options.Add(src_dir);
            batchConvertCommand.Options.Add(base_addr);
            batchConvertCommand.Options.Add(out_dir);
            batchConvertCommand.Options.Add(tx_id);
            batchConvertCommand.Options.Add(rx_id);

            batchConvertCommand.SetAction((ParseResult ctx) =>
            {
                string? batPath = ctx.GetValue(bat_file);
                string? sourceDir = ctx.GetValue(src_dir);
                string odir = ctx.GetValue(out_dir) ?? Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "OutputHex");
                if (!Directory.Exists(odir)) Directory.CreateDirectory(odir);

                List<BatchCommand> batchCmds = new List<BatchCommand>();

                if (!string.IsNullOrEmpty(batPath) && File.Exists(batPath))
                {
                    Console.WriteLine($"Parsing batch file: {batPath}");
                    batchCmds = BatchParser.Parse(batPath);
                }
                else if (!string.IsNullOrEmpty(sourceDir) && Directory.Exists(sourceDir))
                {
                    string addrStr = ctx.GetValue(base_addr)!.Replace("0x", "");
                    uint addr = uint.Parse(addrStr, NumberStyles.HexNumber);
                    Console.WriteLine($"Scanning directory: {sourceDir} for .bin and .rle files...");
                    var files = Directory.GetFiles(sourceDir, "*.*")
                                 .Where(f => f.EndsWith(".bin", StringComparison.OrdinalIgnoreCase) || 
                                             f.EndsWith(".rle", StringComparison.OrdinalIgnoreCase));
                    foreach (var f in files) batchCmds.Add(new BatchCommand { Address = addr, FilePath = f });
                }
                else
                {
                    Console.WriteLine("Error: Either --bat or --src_dir must be valid.");
                    return;
                }

                if (batchCmds.Count == 0) { Console.WriteLine("No files found to convert."); return; }

                List<string> hexFiles = new List<string>();
                foreach (var cmd in batchCmds)
                {
                    if (!File.Exists(cmd.FilePath)) { Console.WriteLine($"Warning: File not found: {cmd.FilePath}"); continue; }
                    
                    string hpath = Path.Combine(odir, $"addr_{cmd.Address:X6}_{Path.GetFileNameWithoutExtension(cmd.FilePath)}.hex");
                    Console.WriteLine($"Converting {Path.GetFileName(cmd.FilePath)} to {Path.GetFileName(hpath)}...");
                    BinToHexConverter.Convert(cmd.FilePath, hpath, cmd.Address);
                    hexFiles.Add(hpath);
                }

                string zfName = !string.IsNullOrEmpty(batPath) ? Path.GetFileNameWithoutExtension(batPath) : "BatchResult";
                string zfPath = Path.Combine(odir, $"{zfName}.zflash");
                ZFlashGenerator.Generate(zfPath, hexFiles, ctx.GetValue(tx_id)!, ctx.GetValue(rx_id)!);
                Console.WriteLine($"Successfully converted {hexFiles.Count} files. ZFlash: {zfPath}");
            });

            root.Add(flashCommand);
            root.Add(snifferCommand);
            root.Add(convertCommand);
            root.Add(batchConvertCommand);

            return await root.Parse(args).InvokeAsync();
        }

        private static (uint dt, uint di, uint ci, uint rid, uint tid, uint arb, uint dat) GetCommonParams(ParseResult ctx, Option<string> dt, Option<uint> di, Option<uint> ci, Option<string> txid, Option<string> rxid, Option<uint> arb, Option<uint> dat)
        {
            return (
                MapDevType(ctx.GetValue(dt)!),
                ctx.GetValue(di),
                ctx.GetValue(ci),
                uint.Parse(ctx.GetValue(rxid)!, NumberStyles.HexNumber),
                uint.Parse(ctx.GetValue(txid)!, NumberStyles.HexNumber),
                ctx.GetValue(arb),
                ctx.GetValue(dat)
            );
        }

        private static async Task RunSnifferWithArgsAsync(ParseResult ctx, uint device_type, uint dev_idx, uint chn_idx, uint rx_id, uint tx_id, uint abit_timing, uint dbit_timing, AppConfig config, Option<string?> didOpt, Option<bool> clrOpt, Option<bool> nwOpt, CancellationToken ct)
        {
            string? didStr = ctx.GetValue(didOpt);
            bool clr = ctx.GetValue(clrOpt);
            bool nw = ctx.GetValue(nwOpt);
            await RunSnifferCommandAsync(device_type, dev_idx, chn_idx, rx_id, tx_id, abit_timing, dbit_timing, didStr, clr, config.Sniffer.Commands, nw, config.Sniffer.SnifferLogFile, ct);
        }

        private static async Task RunSnifferCommandAsync(uint device_type, uint dev_idx, uint chn_idx, uint rx_id, uint tx_id, uint abit_timing, uint dbit_timing, string? didStr, bool clearDtc, List<UdsCommandConfig>? commands, bool newWindow, string logFile, CancellationToken ct)
        {
            using ICanTransport can = new ZlgCanTransport(device_type, dev_idx, chn_idx, abit_timing, dbit_timing);
            var iso = new IsoTpClient(can, txId: tx_id, rxId: rx_id);
            var uds = new UdsClient(iso);

            // 1. CLI Args (Highest priority or processed first)
            if (!string.IsNullOrEmpty(didStr))
            {
                byte did_h = byte.Parse(didStr.Substring(0, 2), NumberStyles.HexNumber);
                byte did_l = byte.Parse(didStr.Substring(2, 2), NumberStyles.HexNumber);
                Console.WriteLine($"[Active] Read DID {didStr}");
                var resp = await uds.ReadDidAsync(did_h, did_l, new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true, CancellationToken: ct));
                Console.WriteLine($"Resp: {BitConverter.ToString(resp)}");
            }

            if (clearDtc)
            {
                Console.WriteLine("[Active] Clear DTC");
                bool cleared = await uds.ClearDtcAsync(new UdsRequestOptions(TimeoutMs: 5000, CancellationToken: ct));
                Console.WriteLine($"Cleared: {cleared}");
            }

            // 2. Configured Commands
            if (commands != null)
            {
                foreach (var cmd in commands)
                {
                    if (cmd.Type == UdsCommandRunType.OneShot)
                    {
                        if (cmd.Service == "0x22" && !string.IsNullOrEmpty(cmd.Did))
                        {
                            string d = cmd.Did.Replace("0x", "").Replace(" ", "");
                            if (d.Length == 4)
                            {
                                byte did_h = byte.Parse(d.Substring(0, 2), NumberStyles.HexNumber);
                                byte did_l = byte.Parse(d.Substring(2, 2), NumberStyles.HexNumber);
                                Console.WriteLine($"[Active Config] Read DID {cmd.Did}");
                                var resp = await uds.ReadDidAsync(did_h, did_l, new UdsRequestOptions(TimeoutMs: 1500, HandleResponsePending: true, CancellationToken: ct));
                                Console.WriteLine($"Resp: {BitConverter.ToString(resp)}");
                            }
                        }
                    }
                    else if (cmd.Type == UdsCommandRunType.Periodically)
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

        private static async Task RunFlashCommandAsync(uint device_type, uint dev_idx, uint chn_idx, uint rx_id, uint tx_id, uint abit_timing, uint dbit_timing, string hexDir, FlashConfig flashConfig, bool verbose, CancellationToken ct)
        {
            using ICanTransport can = new ZlgCanTransport(device_type, dev_idx, chn_idx, abit_timing, dbit_timing);
            var iso = new IsoTpClient(can, txId: tx_id, rxId: rx_id);
            var uds = new UdsClient(iso);
            var flashManager = new FlashManager(uds, flashConfig);

            await flashManager.FlashAsync(hexDir, verbose, ct);
        }

        private static IDisposable? SetupLogging(string? logPath)
        {
            if (string.IsNullOrEmpty(logPath)) return null;

            try
            {
                // Ensure directory exists
                string? dir = Path.GetDirectoryName(Path.GetFullPath(logPath));
                if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir)) Directory.CreateDirectory(dir);

                var fileStream = new FileStream(logPath, FileMode.Create, FileAccess.Write, FileShare.Read);
                var writer = new StreamWriter(fileStream, Encoding.UTF8) { AutoFlush = true };
                var dualWriter = new DualWriter(Console.Out, writer);
                Console.SetOut(dualWriter);
                return new LogDisposer(writer, fileStream);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to setup logging to {logPath}: {ex.Message}");
                return null;
            }
        }

        private class DualWriter : TextWriter
        {
            private readonly TextWriter _console;
            private readonly TextWriter _file;
            public override Encoding Encoding => _console.Encoding;

            public DualWriter(TextWriter console, TextWriter file)
            {
                _console = console;
                _file = file;
            }

            public override void Write(char value) { _console.Write(value); _file.Write(value); }
            public override void Write(string? value) { _console.Write(value); _file.Write(value); }
            public override void WriteLine(string? value) { _console.WriteLine(value); _file.WriteLine(value); }
        }

        private class LogDisposer : IDisposable
        {
            private readonly StreamWriter _writer;
            private readonly FileStream _fs;
            private readonly TextWriter _oldOut;

            public LogDisposer(StreamWriter writer, FileStream fs)
            {
                _writer = writer;
                _fs = fs;
                _oldOut = Console.Out;
            }

            public void Dispose()
            {
                _writer.Flush();
                _writer.Dispose();
                _fs.Dispose();
                // We can't easily restore Console.Out if it was a DualWriter, 
                // but since the app is likely exiting, it's fine.
            }
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
