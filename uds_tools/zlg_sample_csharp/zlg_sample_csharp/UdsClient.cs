using System;
using System.Threading;
using System.Threading.Tasks;

namespace zlg_sample_csharp
{
    /// <summary>
    /// UDS client built on top of IsoTpClient.
    /// Implements the agreed interface with UdsRequestOptions and DiagnosticSessionType.
    /// </summary>
    public class UdsClient : IUdSClient
    {
        private readonly IsoTpClient _iso;

        public UdsClient(IsoTpClient iso) => _iso = iso;

        private static UdsRequestOptions Ensure(UdsRequestOptions? opt) => opt ?? new UdsRequestOptions();

        public async Task<bool> ChangeSessionAsync(Enums.DiagnosticSessionType session, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            byte sub = (byte)session; // enum -> byte
            var request = new byte[] { 0x10, sub };
            var resp = await _iso.RequestAsync(request, cts.Token);

            // Positive response to 0x10 is 0x50 + same subFunction
            return resp.Length >= 2 && resp[0] == 0x50 && resp[1] == sub;
        }

        public async Task<byte[]> ReadDidAsync(byte did_h, byte did_low, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { 0x22, did_h, did_low };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (!opt.HandleResponsePending) return resp;

            // Handle ResponsePending: 7F 22 78
            while (resp.Length >= 3 && resp[0] == 0x7F && resp[1] == 0x22 && resp[2] == 0x78)
            {
                await Task.Delay(200, cts.Token);
                resp = await _iso.ReceiveOnlyAsync(cts.Token);
            }

            return resp;
        }

        public async Task<bool> ClearDtcAsync(UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            // ClearDTC: 0x14, here default group FFFFFF (you can change to 00 00 00 if needed)
            var request = new byte[] { 0x14, 0xFF, 0xFF, 0xFF };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
            {
                // Loop while ECU indicates processing (7F 14 78)
                while (resp.Length >= 3 && resp[0] == 0x7F && resp[1] == 0x14 && resp[2] == 0x78)
                {
                    await Task.Delay(250, cts.Token);
                    resp = await _iso.ReceiveOnlyAsync(cts.Token);
                }
            }

            // Positive response to 0x14 is 0x54
            return resp.Length >= 1 && resp[0] == 0x54;
        }
    }
}
