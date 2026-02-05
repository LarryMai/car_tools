using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    public class FlashManager
    {
        private readonly IUdSClient _uds;
        private readonly SecurityAlgorithm _security = new SecurityAlgorithm();

        public FlashManager(IUdSClient uds)
        {
            _uds = uds;
        }

        public async Task<bool> FlashAsync(string hexDirectory, CancellationToken ct = default)
        {
            var hexFiles = Directory.GetFiles(hexDirectory, "*.hex");
            Array.Sort(hexFiles); // Basic sorting, could be improved to match .zflash order if needed

            Console.WriteLine($"Starting flash sequence for {hexFiles.Length} files...");

            // Wakeup sequence
            Console.WriteLine("Sending wakeup sequence...");
            for (int i = 0; i < 3; i++)
            {
                await _uds.TesterPresentAsync(true, new UdsRequestOptions(TimeoutMs: 100, CancellationToken: ct));
                await Task.Delay(50, ct);
            }

            // 1. Enter Extended Session
            Console.WriteLine("Step 1: Entering Extended Session...");
            if (!await _uds.ChangeSessionAsync(DiagnosticSessionType.ExtendedSession, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct)))
            {
                Console.WriteLine("Failed to enter extended session.");
                return false;
            }

            // 2. Security Access
            Console.WriteLine("Step 2: Performing Security Access...");
            byte[] seed = await _uds.SecurityAccessRequestSeedAsync(1, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct));
            if (seed == null || seed.Length == 0)
            {
                Console.WriteLine("Failed to get seed or already unlocked.");
                // If seed is empty, it might be already unlocked, but let's be cautious.
            }
            else
            {
                byte[] key = _security.GenerateKey(seed, 1);
                if (!await _uds.SecurityAccessSendKeyAsync(1, key, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct)))
                {
                    Console.WriteLine("Security access denied.");
                    return false;
                }
            }

            // 3. Control DTC (Disable)
            Console.WriteLine("Step 3: Disabling DTC...");
            await _uds.ControlDtcSettingAsync(UdsConstants.DtcSettingOff, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct));

            // 4. Communication Control (Disable Rx/Tx)
            Console.WriteLine("Step 4: Disabling Communication...");
            await _uds.CommunicationControlAsync(UdsConstants.DisableRxAndTx, UdsConstants.NetworkManagementAndNormalCommunicationMessages, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct));

            // 5. Flash Files
            foreach (var file in hexFiles)
            {
                Console.WriteLine($"Flashing file: {Path.GetFileName(file)}");
                if (!await FlashHexFileAsync(file, ct))
                {
                    Console.WriteLine($"Failed to flash {file}");
                    return false;
                }
            }

            // 6. ECU Reset
            Console.WriteLine("Step 6: Resetting ECU...");
            await _uds.EcuResetAsync(UdsConstants.SoftReset, new UdsRequestOptions(TimeoutMs: 2000, CancellationToken: ct));

            Console.WriteLine("Flash sequence completed successfully!");
            return true;
        }

        private async Task<bool> FlashHexFileAsync(string filePath, CancellationToken ct)
        {
            var segments = IntelHexParser.Parse(filePath);
            foreach (var segment in segments)
            {
                byte[] data = segment.Data;
                const int blockAlign = 128; // Standard alignment if needed
                if (data.Length % blockAlign != 0)
                {
                    int padLen = blockAlign - (data.Length % blockAlign);
                    byte[] paddedData = new byte[data.Length + padLen];
                    Array.Copy(data, 0, paddedData, 0, data.Length);
                    for (int i = 0; i < padLen; i++) paddedData[data.Length + i] = 0xCC; // Padding byte
                    data = paddedData;
                }

                Console.WriteLine($"  Segment: 0x{segment.StartAddress:X8}, Size: {segment.Data.Length} bytes (Padded to {data.Length})");

                // Request Download
                ushort maxBlockLen = await _uds.RequestDownloadAsync(segment.StartAddress, (uint)data.Length, new UdsRequestOptions(TimeoutMs: 5000, CancellationToken: ct));
                if (maxBlockLen == 0)
                {
                    Console.WriteLine("    Request Download failed.");
                    return false;
                }

                // Transfer Data
                int blockSize = maxBlockLen - 2; // Subtract SID and sequence number
                int totalBlocks = (data.Length + blockSize - 1) / blockSize;

                for (int i = 0; i < totalBlocks; i++)
                {
                    int offset = i * blockSize;
                    int length = Math.Min(blockSize, data.Length - offset);
                    byte[] blockData = new byte[length];
                    Array.Copy(data, offset, blockData, 0, length);

                    byte seq = (byte)((i + 1) % 256);
                    if (!await _uds.TransferDataAsync(seq, blockData, new UdsRequestOptions(TimeoutMs: 5000, CancellationToken: ct)))
                    {
                        Console.WriteLine($"    Transfer Data failed at block {i + 1}/{totalBlocks}.");
                        return false;
                    }

                    if ((i + 1) % 10 == 0 || (i + 1) == totalBlocks)
                    {
                        Console.WriteLine($"    Progress: {i + 1}/{totalBlocks} blocks");
                    }
                }

                // Request Transfer Exit
                if (!await _uds.RequestTransferExitAsync(new UdsRequestOptions(TimeoutMs: 5000, CancellationToken: ct)))
                {
                    Console.WriteLine("    Request Transfer Exit failed.");
                    return false;
                }
            }
            return true;
        }
    }
}