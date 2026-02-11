using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace zlg_sample_csharp
{
    /// <summary>
    /// ISO-TP (ISO 15765-2) client that can send arbitrary length PDUs over CAN using SF/FF/CF/FC.
    /// </summary>
    public class IsoTpClient
    {
        private readonly ICanTransport _can;
        private readonly uint _txId; // tester -> ECU
        private readonly uint _rxId; // ECU -> tester
        private readonly SemaphoreSlim _lock = new SemaphoreSlim(1, 1);
        
        public DateTime LastTxTime { get; private set; } = DateTime.MinValue;

        public IsoTpClient(ICanTransport can, uint txId, uint rxId)
        {
            _can = can;
            _txId = txId;
            _rxId = rxId;
        }

        public async Task<byte[]> RequestAsync(byte[] payload, int timeoutMs, CancellationToken ct, bool verbose = false)
        {
            await _lock.WaitAsync(ct);
            try
            {
                _can.ClearBuffer(); // Clear any noise/stale data from high-load bus before sending
                await SendIsoTp(payload, timeoutMs, ct);
                return await ReceiveIsoTp(timeoutMs, ct, verbose);
            }
            finally
            {
                _lock.Release();
            }
        }

        public async Task SendOnlyAsync(byte[] payload, int timeoutMs, CancellationToken ct)
        {
            await _lock.WaitAsync(ct);
            try
            {
                // Do NOT clear buffer here, as we might be sending a heartbeat while waiting for a response in another context (though strictly speaking, RequestAsync locks so that won't happen concurrently. But we shouldn't clear buffer for just sending.)
                await SendIsoTp(payload, timeoutMs, ct);
            }
            finally
            {
                _lock.Release();
            }
        }

        private async Task SendIsoTp(byte[] data, int timeoutMs, CancellationToken ct)
        {
            LastTxTime = DateTime.Now;
            
            // Ensure at least a reasonable timeout for FC (e.g. 2000ms minimum) if user passed 0 or small value
            int waitFcTimeout = timeoutMs > 2000 ? timeoutMs : 2000;

            if (data.Length <= 7)
            {
                // Single Frame (SF)
                var sf = new byte[8];
                sf[0] = (byte)(0x00 | data.Length);
                Array.Copy(data, 0, sf, 1, data.Length);
                await _can.SendAsync(_txId, sf, ct);
            }
            else
            {
                // First Frame (FF)
                int totalLen = data.Length;
                var ff = new byte[8];
                ff[0] = (byte)(0x10 | ((totalLen >> 8) & 0x0F));
                ff[1] = (byte)(totalLen & 0xFF);
                Array.Copy(data, 0, ff, 2, 6);
                await _can.SendAsync(_txId, ff, ct);

                // Wait Flow Control (FC)
                var (fcId, fcData) = await _can.ReceiveAsync(_rxId, waitFcTimeout, ct);
                if ((fcData[0] & 0xF0) != 0x30)
                    throw new Exception("ISO-TP: expected FC after FF");

                byte blockSize = fcData[1];
                byte stMin = fcData[2];
                if (blockSize == 0) blockSize = 0xFF; // unlimited

                int bytesSent = 6;
                byte sn = 1;
                int blk = 0;

                while (bytesSent < totalLen)
                {
                    int chunk = Math.Min(7, totalLen - bytesSent);
                    var cf = new byte[8];
                    cf[0] = (byte)(0x20 | (sn & 0x0F));
                    Array.Copy(data, bytesSent, cf, 1, chunk);
                    await _can.SendAsync(_txId, cf, ct);

                    bytesSent += chunk;
                    sn++;
                    if (sn > 0x0F) sn = 0;
                    blk++;

                    if (blk >= blockSize)
                    {
                        // Need next FC
                        var (fcId2, fcData2) = await _can.ReceiveAsync(_rxId, waitFcTimeout, ct);
                        if ((fcData2[0] & 0xF0) != 0x30)
                            throw new Exception("ISO-TP: expected FC (mid)");
                        blk = 0;
                    }

                    if (stMin > 0)
                        await Task.Delay(stMin, ct);
                }
            }
        }

        private async Task<byte[]> ReceiveIsoTp(int timeoutMs, CancellationToken ct, bool verbose = false)
        {
            var (id, data) = await _can.ReceiveAsync(_rxId, timeoutMs, ct);
            if (verbose) Console.WriteLine($"[Debug IsoTp] Rx Raw: {BitConverter.ToString(data)}");

            byte pci = data[0];
            byte type = (byte)(pci >> 4);

            if (type == 0x0)
            {
                // Single Frame
                // Check for CAN FD Single Frame (Byte 0 is 0x00, Length is in Byte 1)
                // Note: Standard SF with len=0 is invalid, so 0x00 always implies FD SF if using CAN FD
                if (pci == 0x00 && data.Length > 8)
                {
                    int len = data[1];
                    var resp = new byte[len];
                    Array.Copy(data, 2, resp, 0, len);
                    return resp;
                }
                else
                {
                    // Standard CAN SF
                    int len = pci & 0x0F;
                    var resp = new byte[len];
                    Array.Copy(data, 1, resp, 0, len);
                    return resp;
                }
            }
            else if (type == 0x1)
            {
                int len = ((pci & 0x0F) << 8) | data[1];
                var buffer = new List<byte>(len);
                buffer.AddRange(new ArraySegment<byte>(data, 2, 6));

                // Send FC (CTS)
                var fc = new byte[8];
                fc[0] = 0x30;
                fc[1] = 0x00; // unlimited
                fc[2] = 0x00; // no delay
                await _can.SendAsync(_txId, fc, ct);

                byte expectedSn = 1;
                while (buffer.Count < len)
                {
                    var (cid, cdata) = await _can.ReceiveAsync(_rxId, 1000, ct);
                    byte cfType = (byte)(cdata[0] >> 4);
                    if (cfType != 0x2) throw new Exception("ISO-TP: expected CF");
                    byte sn = (byte)(cdata[0] & 0x0F);
                    if (sn != expectedSn) throw new Exception("ISO-TP: wrong SN");
                    expectedSn++; if (expectedSn > 0x0F) expectedSn = 0;

                    int remain = len - buffer.Count;
                    int chunk = Math.Min(7, remain);
                    buffer.AddRange(new ArraySegment<byte>(cdata, 1, chunk));
                }

                return buffer.ToArray();
            }

            throw new Exception("ISO-TP: unsupported frame type");
        }

        public async Task<byte[]> ReceiveOnlyAsync(int timeoutMs, CancellationToken ct)
        {
            // 直接沿用你類別裡的接收邏輯
            return await ReceiveIsoTp(timeoutMs, ct);
        }
    }
}
