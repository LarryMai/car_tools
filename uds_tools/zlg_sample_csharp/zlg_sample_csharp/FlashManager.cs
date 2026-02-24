using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    public class FlashManager
    {
        private readonly IUdSClient _uds;
        private readonly SecurityAlgorithm _security = new SecurityAlgorithm();

        public FlashManager(IUdSClient uds, FlashConfig? config = null)
        {
            _uds = uds;
            if (config != null)
            {
                var k1 = config.GetAesKey(1);
                if (k1 != null) _security.AesKeyLevel1 = k1;
                var k2 = config.GetAesKey(2);
                if (k2 != null) _security.AesKeyLevel2 = k2;
            }
        }

        public async Task<bool> FlashAsync(string hexDirectory, bool verbose = false, CancellationToken ct = default)
        {
            var hexFiles = Directory.GetFiles(hexDirectory, "*.hex").OrderBy(f => f).ToList();
            if (hexFiles.Count == 0)
            {
                Console.WriteLine("No HEX files found in directory.");
                return false;
            }

            Console.WriteLine($"Starting flash sequence for {hexFiles.Count} files...");
            var totalSw = System.Diagnostics.Stopwatch.StartNew();

            try
            {
                // Step 0: Wakeup
                Console.WriteLine("Sending wakeup sequence...");
                for (int i = 0; i < 3; i++)
                {
                    await _uds.TesterPresentAsync(true, new UdsRequestOptions(TimeoutMs: 100, Verbose: verbose, CancellationToken: ct));
                    await Task.Delay(50, ct);
                }

                // Step 1: Extended Session
                Console.WriteLine("Step 1: Entering Extended Session...");
                if (!await _uds.ChangeSessionAsync(DiagnosticSessionType.ExtendedSession, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct)))
                {
                    Console.WriteLine("Failed to enter extended session.");
                    return false;
                }
                await Task.Delay(500, ct);

                // Step 2: Security Access
                Console.WriteLine("Step 2: Performing Security Access...");
                byte[] seed = await _uds.SecurityAccessRequestSeedAsync(1, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));
                if (seed == null || seed.Length == 0)
                {
                    Console.WriteLine("Failed to get seed. ECU might be locked.");
                    return false;
                }
                else
                {
                    byte[] key = _security.GenerateKey(seed, 1);
                    if (!await _uds.SecurityAccessSendKeyAsync(1, key, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct)))
                    {
                        Console.WriteLine("Security access denied.");
                        return false;
                    }
                    Console.WriteLine("✓ Security Access successful.");
                }

                // Step 3: Control DTC (Disable)
                Console.WriteLine("Step 3: Disabling DTC...");
                await _uds.ControlDtcSettingAsync(UdsConstants.DtcSettingOff, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));

                // Step 4: Communication Control (Disable Rx/Tx)
                Console.WriteLine("Step 4: Disabling Communication...");
                await _uds.CommunicationControlAsync(UdsConstants.DisableRxAndTx, UdsConstants.NetworkManagementAndNormalCommunicationMessages, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));

                // Step 5: Flash Files
                int fileIndex = 0;
                foreach (var file in hexFiles)
                {
                    fileIndex++;
                    Console.WriteLine($"[{fileIndex}/{hexFiles.Count}] Flashing file: {Path.GetFileName(file)}");
                    var fileSw = System.Diagnostics.Stopwatch.StartNew();
                    
                    int retryCount = 0;
                    bool fileSuccess = false;
                    while (retryCount < 3 && !fileSuccess)
                    {
                        try
                        {
                            // ONLY re-ensure session/security if this is a RETRY
                            if (retryCount > 0)
                            {
                                Console.WriteLine($"  [Retry {retryCount}] Re-ensuring Extended Session and Security Access...");
                                await _uds.ChangeSessionAsync(DiagnosticSessionType.ExtendedSession, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));
                                byte[] s = await _uds.SecurityAccessRequestSeedAsync(1, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));
                                if (s != null && s.Length > 0)
                                {
                                    byte[] k = _security.GenerateKey(s, 1);
                                    await _uds.SecurityAccessSendKeyAsync(1, k, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));
                                }
                            }

                            fileSuccess = await FlashHexFileAsync(file, verbose, ct, 15000); // 15s timeout for erase/download
                        }
                        catch (Exception ex)
                        {
                            retryCount++;
                            Console.WriteLine($"\n[Error] Failed to flash {Path.GetFileName(file)} (Attempt {retryCount}/3): {ex.Message}");
                            if (retryCount < 3)
                            {
                                Console.WriteLine("Waiting 2 seconds before retrying this file...");
                                await Task.Delay(2000, ct);
                            }
                        }
                    }

                    if (!fileSuccess)
                    {
                        Console.WriteLine($"\n[CRITICAL] Aborting sequence due to persistent failure in: {file}");
                        return false;
                    }

                    fileSw.Stop();
                    Console.WriteLine($"✓ File {fileIndex} finished in {fileSw.Elapsed.TotalSeconds:F2}s");
                }

                // Step 6: ECU Reset
                Console.WriteLine("Step 6: Resetting ECU...");
                await _uds.EcuResetAsync(UdsConstants.SoftReset, new UdsRequestOptions(TimeoutMs: 2000, Verbose: verbose, CancellationToken: ct));

                totalSw.Stop();
                Console.WriteLine($"\n🎉 Flash sequence completed successfully in {totalSw.Elapsed.TotalMinutes:F1} minutes ({totalSw.Elapsed.TotalSeconds:F1}s)!");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n[Fatal] Flash sequence interrupted by unhandled error: {ex.Message}");
                return false;
            }
        }

        private async Task<bool> FlashHexFileAsync(string filePath, bool verbose, CancellationToken ct, int downloadTimeoutMs = 5000)
        {
            var segments = IntelHexParser.Parse(filePath);
            foreach (var segment in segments)
            {
                byte[] data = segment.Data;
                const int blockAlign = 128; 
                if (data.Length % blockAlign != 0)
                {
                    int padLen = blockAlign - (data.Length % blockAlign);
                    byte[] paddedData = new byte[data.Length + padLen];
                    Array.Copy(data, 0, paddedData, 0, data.Length);
                    for (int i = 0; i < padLen; i++) paddedData[data.Length + i] = 0xCC; 
                    data = paddedData;
                }

                Console.WriteLine($"  Segment: 0x{segment.StartAddress:X8}, Size: {segment.Data.Length} bytes (Padded to {data.Length})");

                // Request Download (SID 0x34)
                ushort maxBlockLen = await _uds.RequestDownloadAsync(segment.StartAddress, (uint)data.Length, new UdsRequestOptions(TimeoutMs: downloadTimeoutMs, HandleResponsePending: true, Verbose: verbose, CancellationToken: ct));
                if (maxBlockLen == 0)
                {
                    Console.WriteLine("    Request Download failed.");
                    return false;
                }

                // Transfer Data (SID 0x36)
                int blockSize = maxBlockLen - 2; 
                int totalBlocks = (data.Length + blockSize - 1) / blockSize;

                for (int i = 0; i < totalBlocks; i++)
                {
                    int offset = i * blockSize;
                    int length = Math.Min(blockSize, data.Length - offset);
                    byte[] blockData = new byte[length];
                    Array.Copy(data, offset, blockData, 0, length);

                    byte seq = (byte)((i + 1) % 256);
                    
                    // We add a small retry inside TransferData for transient bus errors
                    int blockRetry = 0;
                    bool blockSuccess = false;
                    while (blockRetry < 2 && !blockSuccess)
                    {
                        try 
                        {
                            // 20s timeout to allow for Response Pending (0x78) loops and long write times
                            byte nrc = await _uds.TransferDataAsync(seq, blockData, new UdsRequestOptions(TimeoutMs: 20000, HandleResponsePending: true, Verbose: verbose, CancellationToken: ct));
                            
                            if (nrc == 0x00)
                            {
                                blockSuccess = true;
                            }
                            else if (nrc == 0x73 && blockRetry > 0)
                            {
                                // NRC 0x73 (WrongBlockSequenceCounter) on a RETRY implies the ECU
                                // already received the previous attempt successfully but we missed the ACK.
                                // We treat this as success to avoid getting stuck or aborting.
                                Console.WriteLine($"    [Info] Block {i + 1} retry got NRC 0x73 (Sequence Error). Assuming previous attempt succeeded.");
                                blockSuccess = true;
                            }
                            else
                            {
                                Console.WriteLine($"    [Error] Block {i + 1} failed with NRC: 0x{nrc:X2}");
                                blockSuccess = false; // Will trigger retry loop
                                throw new Exception($"NRC 0x{nrc:X2}"); // Throw to trigger catch block for retry logic
                            }
                        }
                        catch (Exception ex) when (ex is TimeoutException || ex is OperationCanceledException || ex is TaskCanceledException || ex.Message.Contains("NRC"))
                        {
                            blockRetry++;
                            if (blockRetry < 2) await Task.Delay(100, ct);
                        }
                    }

                    if (!blockSuccess)
                    {
                        Console.WriteLine($"    Transfer Data failed at block {i + 1}/{totalBlocks}.");
                        return false;
                    }

                    if ((i + 1) % 50 == 0 || (i + 1) == totalBlocks)
                    {
                        Console.WriteLine($"    Progress: {i + 1}/{totalBlocks} blocks");
                    }
                }

                // Request Transfer Exit (SID 0x37)
                if (!await _uds.RequestTransferExitAsync(new UdsRequestOptions(TimeoutMs: 5000, HandleResponsePending: true, Verbose: verbose, CancellationToken: ct)))
                {
                    Console.WriteLine("    Request Transfer Exit failed.");
                    return false;
                }
            }
            return true;
        }
    }
}