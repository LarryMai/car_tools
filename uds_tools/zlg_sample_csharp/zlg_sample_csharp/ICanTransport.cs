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
        
        /// <summary>
        /// Receives a CAN frame.
        /// </summary>
        /// <param name="expectedCanId">If null, receives any frame. If set, filters by ID.</param>
        /// <returns>Tuple of (CAN ID, Data)</returns>
        Task<(uint canId, byte[] data)> ReceiveAsync(uint? expectedCanId, int timeoutMs, CancellationToken ct);

        /// <summary>
        /// Clears the receive buffer.
        /// </summary>
        void ClearBuffer();
    }
}
