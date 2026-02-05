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
        CancellationToken CancellationToken = default
    );

    public interface IUdSClient
    {
        Task<byte[]> ReadDidAsync(byte did_h, byte did_low, UdsRequestOptions? options = null);
        Task<bool> ClearDtcAsync(UdsRequestOptions? options = null);
        Task<bool> ChangeSessionAsync(Enums.DiagnosticSessionType session, UdsRequestOptions? options = null);
    }
}
