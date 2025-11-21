using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace zlg_sample_csharp.Enums
{
    /// <summary>Session 可用性（可複選）</summary>
    [Flags]
    public enum DiagnosticSessionMask : byte
    {
        None = 0,
        Default = 1 << 0,
        Programming = 1 << 1,
        Extended = 1 << 2,
        All = Default | Programming | Extended
    }

    /// <summary>UDS 診斷 Session 類型（0x10 的子功能值）</summary>
    public enum DiagnosticSessionType : byte
    {
        DefaultSession = 0x01, // 0x10 0x01 → 正回應 0x50 0x01
        ProgrammingSession = 0x02, // 0x10 0x02 → 正回應 0x50 0x02
        ExtendedSession = 0x03, // 0x10 0x03 → 正回應 0x50 0x03
    }
}
