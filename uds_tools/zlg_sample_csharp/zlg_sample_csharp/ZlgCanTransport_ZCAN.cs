using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;
using ZLGAPI; // requires ZLGAPI_fixed.cs (namespace ZLGAPI, class ZLGCAN)

namespace zlg_sample_csharp
{
    public enum ZcanBusMode
    {
        Can = 0,   // Classic CAN (8 bytes)
        CanFd = 1  // CAN FD (up to 64 bytes)
    }

    /// <summary>
    /// One-file universal ZLG CAN/CAN-FD transport built on ZLGCAN.ZCAN_* APIs.
    /// - Choose Classic CAN or CAN FD via constructor parameter.
    /// - Implements ICanTransport for both modes.
    /// </summary>
    public sealed class ZlgCanTransport : ICanTransport, IDisposable
    {
        private readonly uint _devType;
        private readonly uint _devIndex;
        private readonly uint _canIndex;
        private readonly ZcanBusMode _mode;

        // Classic CAN timing
        private readonly byte _timing0;
        private readonly byte _timing1;

        // CAN FD timing (SDK-specific packed values)
        private readonly uint _arbBtr;
        private readonly uint _dataBtr;

        private IntPtr _devHandle = IntPtr.Zero;
        private IntPtr _chnHandle = IntPtr.Zero;

        /// <summary>
        /// Classic CAN constructor.
        /// </summary>
        public ZlgCanTransport(uint devType, uint devIndex, uint canIndex,
                                         byte abit_timing, byte dbit_timing, byte mode = 0)
        {
            _devType = devType;
            _devIndex = devIndex;
            _canIndex = canIndex;
            _mode = ZcanBusMode.Can;
            _timing0 = abit_timing;
            _timing1 = dbit_timing;

            OpenAndInitClassic(mode);
        }

        /// <summary>
        /// CAN FD constructor.
        /// </summary>
        public ZlgCanTransport(uint devType, uint devIndex, uint canIndex,
                                         uint arbBtr, uint dataBtr, byte mode = 0)
        {
            _devType = devType;
            _devIndex = devIndex;
            _canIndex = canIndex;
            _mode = ZcanBusMode.CanFd;
            _arbBtr = arbBtr;
            _dataBtr = dataBtr;

            OpenAndInitFd(mode);
        }

        private void OpenDevice()
        {
            _devHandle = ZLGCAN.ZCAN_OpenDevice(_devType, _devIndex, 0);
            if (_devHandle == IntPtr.Zero)
                throw new Exception("ZCAN_OpenDevice failed.");
        }

        private void OpenAndInitClassic(byte mode)
        {
            OpenDevice();

            var canCfg = new ZLGCAN._ZCAN_CHANNEL_CAN_INIT_CONFIG
            {
                acc_code = 0,
                acc_mask = 0xFFFFFFFF,
                reserved = 0,
                filter = 1,
                timing0 = _timing0,
                timing1 = _timing1,
                mode = mode
            };

            var union = new ZLGCAN._ZCAN_CHANNEL_INIT_CONFIG { can = canCfg };
            var init = new ZLGCAN.ZCAN_CHANNEL_INIT_CONFIG { can_type = 0, config = union };

            int size = Marshal.SizeOf<ZLGCAN.ZCAN_CHANNEL_INIT_CONFIG>();
            IntPtr pInit = Marshal.AllocHGlobal(size);
            try
            {
                Marshal.StructureToPtr(init, pInit, false);
                _chnHandle = ZLGCAN.ZCAN_InitCAN(_devHandle, _canIndex, pInit);
                if (_chnHandle == IntPtr.Zero)
                    throw new Exception("ZCAN_InitCAN (CAN) failed.");
            }
            finally
            {
                Marshal.FreeHGlobal(pInit);
            }

            if (ZLGCAN.ZCAN_StartCAN(_chnHandle) == 0)
                throw new Exception("ZCAN_StartCAN failed.");
        }

        private void OpenAndInitFd(byte mode)
        {
            OpenDevice();

            var fdCfg = new ZLGCAN._ZCAN_CHANNEL_CANFD_INIT_CONFIG
            {
                acc_code = 0,
                acc_mask = 0xFFFFFFFF,
                reserved = 0,
                filter = 1,
                mode = mode,
                abit_timing = _arbBtr,
                dbit_timing = _dataBtr
            };

            var union = new ZLGCAN._ZCAN_CHANNEL_INIT_CONFIG { canfd = fdCfg };
            var init = new ZLGCAN.ZCAN_CHANNEL_INIT_CONFIG { can_type = 1, config = union };

            int size = Marshal.SizeOf<ZLGCAN.ZCAN_CHANNEL_INIT_CONFIG>();
            IntPtr pInit = Marshal.AllocHGlobal(size);
            try
            {
                Marshal.StructureToPtr(init, pInit, false);
                _chnHandle = ZLGCAN.ZCAN_InitCAN(_devHandle, _canIndex, pInit);
                if (_chnHandle == IntPtr.Zero)
                    throw new Exception("ZCAN_InitCAN (FD) failed.");
            }
            finally
            {
                Marshal.FreeHGlobal(pInit);
            }

            if (ZLGCAN.ZCAN_StartCAN(_chnHandle) == 0)
                throw new Exception("ZCAN_StartCAN failed.");
        }

        public Task SendAsync(uint canId, byte[] data, CancellationToken ct)
        {
            if (_chnHandle == IntPtr.Zero) throw new InvalidOperationException("CAN channel not opened.");
            if (data == null) throw new ArgumentNullException(nameof(data));

            if (_mode == ZcanBusMode.Can)
            {
                if (data.Length > 8) throw new ArgumentException("Classic CAN frame cannot exceed 8 bytes.");

                var frame = new ZLGCAN.can_frame
                {
                    can_id = canId,
                    can_dlc = (byte)data.Length,
                    __pad = 0,
                    __res0 = 0,
                    __res1 = 0,
                    data = new byte[8]
                };
                Array.Copy(data, frame.data, data.Length);

                var tx = new ZLGCAN.ZCAN_Transmit_Data
                {
                    frame = frame,
                    transmit_type = 0
                };

                int size = Marshal.SizeOf<ZLGCAN.ZCAN_Transmit_Data>();
                IntPtr pTx = Marshal.AllocHGlobal(size);
                try
                {
                    Marshal.StructureToPtr(tx, pTx, false);
                    uint sent = ZLGCAN.ZCAN_Transmit(_chnHandle, pTx, 1);
                    if (sent == 0) throw new Exception("ZCAN_Transmit failed.");
                }
                finally
                {
                    Marshal.FreeHGlobal(pTx);
                }
            }
            else
            {
                if (data.Length > 64) throw new ArgumentException("CAN FD frame cannot exceed 64 bytes.");
                var frame = new ZLGCAN.canfd_frame
                {
                    can_id = canId,
                    len = (byte)data.Length,
                    flags = 0, // set BRS/ESI as needed
                    __res0 = 0,
                    __res1 = 0,
                    data = new byte[64]
                };
                Array.Copy(data, frame.data, data.Length);

                var tx = new ZLGCAN.ZCAN_TransmitFD_Data
                {
                    frame = frame,
                    transmit_type = 0
                };

                int size = Marshal.SizeOf<ZLGCAN.ZCAN_TransmitFD_Data>();
                IntPtr pTx = Marshal.AllocHGlobal(size);
                try
                {
                    Marshal.StructureToPtr(tx, pTx, false);
                    uint sent = ZLGCAN.ZCAN_TransmitFD(_chnHandle, pTx, 1);
                    if (sent == 0)
                    {
                        Console.WriteLine($"[Debug] ZCAN_TransmitFD failed for ID: 0x{canId:X}, Len: {data.Length}. Hardware Error: {GetErrorInfo()}");
                        throw new Exception("ZCAN_TransmitFD failed.");
                    }
                }
                finally
                {
                    Marshal.FreeHGlobal(pTx);
                }
            }

            return Task.CompletedTask;
        }

        private string GetErrorInfo()
        {
            if (_chnHandle == IntPtr.Zero) return "Channel not open";

            int size = Marshal.SizeOf<ZLGCAN.ZCAN_CHANNEL_ERR_INFO>();
            IntPtr pErr = Marshal.AllocHGlobal(size);
            try
            {
                if (ZLGCAN.ZCAN_ReadChannelErrInfo(_chnHandle, pErr) == 1)
                {
                    var info = Marshal.PtrToStructure<ZLGCAN.ZCAN_CHANNEL_ERR_INFO>(pErr);
                    return $"Code=0x{info.error_code:X8}, Passive={BitConverter.ToString(info.passive_ErrData)}, ArbiLost=0x{info.arbi_lost_ErrData:X2}";
                }
                return "Failed to read error info";
            }
            catch (Exception ex)
            {
                return $"Ex: {ex.Message}";
            }
            finally
            {
                Marshal.FreeHGlobal(pErr);
            }
        }

        public async Task<(uint canId, byte[] data)> ReceiveAsync(uint? expectedCanId, int timeoutMs, CancellationToken ct)
        {
            if (_chnHandle == IntPtr.Zero) throw new InvalidOperationException("CAN channel not opened.");
            var start = Environment.TickCount;

            if (_mode == ZcanBusMode.Can)
            {
                int oneSize = Marshal.SizeOf<ZLGCAN.ZCAN_Receive_Data>();
                int count = 64;
                IntPtr pBuf = Marshal.AllocHGlobal(oneSize * count);
                try
                {
                    while (true)
                    {
                        ct.ThrowIfCancellationRequested();
                        uint got = ZLGCAN.ZCAN_Receive(_chnHandle, pBuf, (uint)count, 10);
                        if (got > 0)
                        {
                            for (int i = 0; i < got; i++)
                            {
                                IntPtr pItem = pBuf + i * oneSize;
                                var item = Marshal.PtrToStructure<ZLGCAN.ZCAN_Receive_Data>(pItem);
                                if (item != null && item.frame != null)
                                {
                                    if (expectedCanId == null || item.frame.can_id == expectedCanId)
                                    {
                                        var len = Math.Min((int)item.frame.can_dlc, 8);
                                        var payload = new byte[len];
                                        Array.Copy(item.frame.data, payload, len);
                                        return (item.frame.can_id, payload);
                                    }
                                }
                            }
                        }

                        if (timeoutMs > 0 && Environment.TickCount - start > timeoutMs)
                            throw new TimeoutException($"ZCAN receive timeout. Hardware Status: {GetErrorInfo()}");

                        await Task.Delay(1, ct);
                    }
                }
                finally
                {
                    Marshal.FreeHGlobal(pBuf);
                }
            }
            else
            {
                int oneSize = Marshal.SizeOf<ZLGCAN.ZCAN_ReceiveFD_Data>();
                int count = 64;
                IntPtr pBuf = Marshal.AllocHGlobal(oneSize * count);
                try
                {
                    while (true)
                    {
                        ct.ThrowIfCancellationRequested();
                        uint got = ZLGCAN.ZCAN_ReceiveFD(_chnHandle, pBuf, (uint)count, 10);
                        if (got > 0)
                        {
                            for (int i = 0; i < got; i++)
                            {
                                IntPtr pItem = pBuf + i * oneSize;
                                var item = Marshal.PtrToStructure<ZLGCAN.ZCAN_ReceiveFD_Data>(pItem);
                                if (item != null && item.frame != null)
                                {
                                    if (expectedCanId == null || item.frame.can_id == expectedCanId)
                                    {
                                        var len = Math.Min((int)item.frame.len, 64);
                                        var payload = new byte[len];
                                        Array.Copy(item.frame.data, payload, len);
                                        return (item.frame.can_id, payload);
                                    }
                                }
                            }
                        }

                        if (timeoutMs > 0 && Environment.TickCount - start > timeoutMs)
                            throw new TimeoutException($"ZCAN receive timeout. Hardware Status: {GetErrorInfo()}");

                        await Task.Delay(1, ct);
                    }
                }
                finally
                {
                    Marshal.FreeHGlobal(pBuf);
                }
            }
        }

        public void Dispose()
        {
            if (_chnHandle != IntPtr.Zero)
            {
                ZLGCAN.ZCAN_ResetCAN(_chnHandle);
                _chnHandle = IntPtr.Zero;
            }
            if (_devHandle != IntPtr.Zero)
            {
                ZLGCAN.ZCAN_CloseDevice(_devHandle);
                _devHandle = IntPtr.Zero;
            }
        }
    }
}
