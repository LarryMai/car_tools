using System;
using System.Threading;
using System.Threading.Tasks;
using zlg_sample_csharp.Enums;

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

        private async Task<byte[]> HandleResponsePendingAsync(byte[] resp, UdsService requestSid, CancellationToken ct)
        {
            // Handle ResponsePending: 7F [SID] 78
            while (resp.Length >= 3 && resp[0] == (byte)UdsNrc.ServiceNotSupportedInActiveSession && resp[1] == (byte)requestSid && resp[2] == (byte)UdsNrc.RequestCorrectlyReceivedResponsePending)
            {
                await Task.Delay(200, ct);
                resp = await _iso.ReceiveOnlyAsync(ct);
            }
            return resp;
        }

        public async Task<bool> ChangeSessionAsync(DiagnosticSessionType session, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            byte sub = (byte)session;
            var request = new byte[] { (byte)UdsService.DiagnosticSessionControl, sub };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.DiagnosticSessionControl, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.DiagnosticSessionControl.PositiveResponseSid() && resp[1] == sub;
        }

        public async Task<byte[]> ReadDidAsync(byte did_h, byte did_low, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.ReadDataByIdentifier, did_h, did_low };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.ReadDataByIdentifier, cts.Token);

            return resp;
        }

        public async Task<bool> ClearDtcAsync(UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.ClearDiagnosticInformation, 0xFF, 0xFF, 0xFF };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.ClearDiagnosticInformation, cts.Token);

            return resp.Length >= 1 && resp[0] == UdsService.ClearDiagnosticInformation.PositiveResponseSid();
        }

        public async Task<byte[]> SecurityAccessRequestSeedAsync(byte level, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.SecurityAccess, level };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.SecurityAccess, cts.Token);

            if (resp.Length >= 2 && resp[0] == UdsService.SecurityAccess.PositiveResponseSid() && resp[1] == level)
            {
                byte[] seed = new byte[resp.Length - 2];
                Array.Copy(resp, 2, seed, 0, seed.Length);
                return seed;
            }
            return Array.Empty<byte>();
        }

        public async Task<bool> SecurityAccessSendKeyAsync(byte level, byte[] key, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            byte sub = (byte)(level + 1);
            var request = new byte[2 + key.Length];
            request[0] = (byte)UdsService.SecurityAccess;
            request[1] = sub;
            Array.Copy(key, 0, request, 2, key.Length);

            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.SecurityAccess, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.SecurityAccess.PositiveResponseSid() && resp[1] == sub;
        }

        public async Task<bool> CommunicationControlAsync(byte controlType, byte communicationType, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.CommunicationControl, controlType, communicationType };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.CommunicationControl, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.CommunicationControl.PositiveResponseSid() && resp[1] == controlType;
        }

        public async Task<bool> ControlDtcSettingAsync(byte settingType, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.ControlDTCSetting, settingType };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.ControlDTCSetting, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.ControlDTCSetting.PositiveResponseSid() && resp[1] == settingType;
        }

        public async Task<ushort> RequestDownloadAsync(uint address, uint size, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            // addressAndLengthFormatIdentifier = 0x44 (4 bytes address, 4 bytes size)
            var request = new byte[]
            {
                (byte)UdsService.RequestDownload, 0x00, 0x44,
                (byte)((address >> 24) & 0xFF), (byte)((address >> 16) & 0xFF), (byte)((address >> 8) & 0xFF), (byte)(address & 0xFF),
                (byte)((size >> 24) & 0xFF), (byte)((size >> 16) & 0xFF), (byte)((size >> 8) & 0xFF), (byte)(size & 0xFF)
            };

            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.RequestDownload, cts.Token);

            if (resp.Length >= 4 && resp[0] == UdsService.RequestDownload.PositiveResponseSid())
            {
                // lengthFormatIdentifier is usually bits [7:4] of resp[1]
                // but we mostly care about maxNumberOfBlockLength in resp[2] and resp[3]
                return (ushort)((resp[2] << 8) | resp[3]);
            }
            return 0;
        }

        public async Task<bool> TransferDataAsync(byte sequenceNumber, byte[] data, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[2 + data.Length];
            request[0] = (byte)UdsService.TransferData;
            request[1] = sequenceNumber;
            Array.Copy(data, 0, request, 2, data.Length);

            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.TransferData, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.TransferData.PositiveResponseSid() && resp[1] == sequenceNumber;
        }

        public async Task<bool> RequestTransferExitAsync(UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.RequestTransferExit };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.RequestTransferExit, cts.Token);

            return resp.Length >= 1 && resp[0] == UdsService.RequestTransferExit.PositiveResponseSid();
        }

        public async Task<bool> EcuResetAsync(byte resetType, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            var request = new byte[] { (byte)UdsService.ECUReset, resetType };
            var resp = await _iso.RequestAsync(request, cts.Token);

            if (opt.HandleResponsePending)
                resp = await HandleResponsePendingAsync(resp, UdsService.ECUReset, cts.Token);

            return resp.Length >= 2 && resp[0] == UdsService.ECUReset.PositiveResponseSid() && resp[1] == resetType;
        }

        public async Task TesterPresentAsync(bool suppressResponse = true, UdsRequestOptions? options = null)
        {
            var opt = Ensure(options);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(opt.CancellationToken);
            if (opt.TimeoutMs > 0) cts.CancelAfter(opt.TimeoutMs);

            byte sub = (byte)(suppressResponse ? 0x80 : 0x00);
            var request = new byte[] { (byte)UdsService.TesterPresent, sub };

            if (suppressResponse)
            {
                // Just send, don't wait for response
                // We need a way to just send in IsoTpClient?
                // For now, let's use RequestAsync but ignore result if it times out
                try
                {
                    await _iso.RequestAsync(request, cts.Token);
                }
                catch
                {
                    // Ignore
                }
            }
            else
            {
                var resp = await _iso.RequestAsync(request, cts.Token);
                if (opt.HandleResponsePending)
                    await HandleResponsePendingAsync(resp, UdsService.TesterPresent, cts.Token);
            }
        }
    }
}
