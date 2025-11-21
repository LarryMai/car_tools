using System;
using System.Threading;
using System.Threading.Tasks;

namespace zlg_sample_csharp
{
    /// <summary>
    /// Minimal CAN transport abstraction.
    /// </summary>
    public interface ICanTransport : IDisposable
    {
        Task SendAsync(uint canId, byte[] data, CancellationToken ct);
        Task<(uint canId, byte[] data)> ReceiveAsync(uint expectedCanId, int timeoutMs, CancellationToken ct);
    }
}
