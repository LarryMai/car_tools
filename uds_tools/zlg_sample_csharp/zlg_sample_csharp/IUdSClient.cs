using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace zlg_sample_csharp
{

    public record UdsRequestOptions(
        int TimeoutMs = 1000,
        bool HandleResponsePending = true,
        bool Verbose = false,
        CancellationToken CancellationToken = default
    );

    public interface IUdSClient
    {
        Task<byte[]> ReadDidAsync(byte did_h, byte did_low, UdsRequestOptions? options = null);
        Task<bool> ClearDtcAsync(UdsRequestOptions? options = null);
        Task<bool> ChangeSessionAsync(Enums.DiagnosticSessionType session, UdsRequestOptions? options = null);
        Task<byte[]> SecurityAccessRequestSeedAsync(byte level, UdsRequestOptions? options = null);
        Task<bool> SecurityAccessSendKeyAsync(byte level, byte[] key, UdsRequestOptions? options = null);
        Task<bool> CommunicationControlAsync(byte controlType, byte communicationType, UdsRequestOptions? options = null);
        Task<bool> ControlDtcSettingAsync(byte settingType, UdsRequestOptions? options = null);
        Task<ushort> RequestDownloadAsync(uint address, uint size, UdsRequestOptions? options = null);
        Task<byte> TransferDataAsync(byte sequenceNumber, byte[] data, UdsRequestOptions? options = null);
        Task<bool> RequestTransferExitAsync(UdsRequestOptions? options = null);
        Task<bool> EcuResetAsync(byte resetType, UdsRequestOptions? options = null);
        Task TesterPresentAsync(bool suppressResponse = true, UdsRequestOptions? options = null);
        
        DateTime LastActivityTime { get; }
    }
}
