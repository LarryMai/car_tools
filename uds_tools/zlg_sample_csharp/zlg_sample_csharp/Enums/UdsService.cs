using System;
using System.Collections.Generic;

namespace zlg_sample_csharp.Enums
{
    /// <summary>UDS Service ID (SID)</summary>
    public enum UdsService : byte
    {
        // Diagnostic & Communication Management
        DiagnosticSessionControl = 0x10, // DSC
        ECUReset = 0x11, // ER
        SecurityAccess = 0x27, // SA
        CommunicationControl = 0x28, // CC
        TesterPresent = 0x3E, // TP
        AccessTimingParameter = 0x83, // ATP
        SecuredDataTransmission = 0x84, // SDT
        ControlDTCSetting = 0x85, // CDTCS
        ResponseOnEvent = 0x86, // ROE
        LinkControl = 0x87, // LC

        // Data Transmission
        ReadDataByIdentifier = 0x22, // RDBI
        ReadMemoryByAddress = 0x23, // RMBA
        ReadScalingDataByIdentifier = 0x24, // RSDBI
        ReadDataByPeriodicIdentifier = 0x2A, // RDBPI
        DynamicallyDefineDataIdentifier = 0x2C, // DDDI
        WriteDataByIdentifier = 0x2E, // WDBI
        WriteMemoryByAddress = 0x3D, // WMBA

        // Stored Data Transmission
        ClearDiagnosticInformation = 0x14, // CDTCI
        ReadDTCInformation = 0x19, // RDTCI

        // Input / Output Control
        InputOutputControlByIdentifier = 0x2F, // IOCBI

        // Remote Activation of Routine
        RoutineControl = 0x31, // RC

        // Upload & Download
        RequestDownload = 0x34, // RD
        RequestUpload = 0x35, // RU
        TransferData = 0x36, // TD
        RequestTransferExit = 0x37  // RTSE
    }

    /// <summary>服務能力標記（可複選）</summary>
    [Flags]
    public enum UdsServiceCapability : ushort
    {
        None = 0,
        HasSubFunction = 1 << 0,
        DataTransmission = 1 << 1,
        StoredData = 1 << 2,
        IoControl = 1 << 3,
        Routine = 1 << 4,
        DownloadUpload = 1 << 5,
        CommMgmt = 1 << 6,
        RoeRelated = 1 << 7,
    }

    public sealed record UdsServiceInfo(
        UdsService Service,
        string Mnemonic,
        string English,
        string Chinese,
        DiagnosticSessionMask AllowedSessions,
        UdsServiceCapability Capabilities
    );

    public static class UdsServiceCatalog
    {
        // 典型（可依 ECU 規格覆寫）
        private static readonly Dictionary<UdsService, UdsServiceInfo> _db = new()
        {
            // --- Management
            [UdsService.DiagnosticSessionControl] = new(UdsService.DiagnosticSessionControl, "DSC",
                "DiagnosticSessionControl", "診斷會談控制",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.ECUReset] = new(UdsService.ECUReset, "ER",
                "ECUReset", "ECU 重置",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.SecurityAccess] = new(UdsService.SecurityAccess, "SA",
                "SecurityAccess", "安全存取",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.CommunicationControl] = new(UdsService.CommunicationControl, "CC",
                "CommunicationControl", "通訊控制",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.TesterPresent] = new(UdsService.TesterPresent, "TP",
                "TesterPresent", "測試器在線",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.AccessTimingParameter] = new(UdsService.AccessTimingParameter, "ATP",
                "AccessTimingParameter", "時序參數存取",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.CommMgmt),

            [UdsService.SecuredDataTransmission] = new(UdsService.SecuredDataTransmission, "SDT",
                "SecuredDataTransmission", "安全資料傳輸",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.CommMgmt),

            [UdsService.ControlDTCSetting] = new(UdsService.ControlDTCSetting, "CDTCS",
                "ControlDTCSetting", "DTC 控制設定",
                DiagnosticSessionMask.All, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            [UdsService.ResponseOnEvent] = new(UdsService.ResponseOnEvent, "ROE",
                "ResponseOnEvent", "事件回應",
                DiagnosticSessionMask.Extended, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction | UdsServiceCapability.RoeRelated),

            [UdsService.LinkControl] = new(UdsService.LinkControl, "LC",
                "LinkControl", "連結控制",
                DiagnosticSessionMask.Extended, UdsServiceCapability.CommMgmt | UdsServiceCapability.HasSubFunction),

            // --- Data Transmission
            [UdsService.ReadDataByIdentifier] = new(UdsService.ReadDataByIdentifier, "RDBI",
                "ReadDataByIdentifier", "讀取資料識別碼",
                DiagnosticSessionMask.Default | DiagnosticSessionMask.Extended, UdsServiceCapability.DataTransmission),

            [UdsService.ReadMemoryByAddress] = new(UdsService.ReadMemoryByAddress, "RMBA",
                "ReadMemoryByAddress", "讀取記憶體位址",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.DataTransmission),

            [UdsService.ReadScalingDataByIdentifier] = new(UdsService.ReadScalingDataByIdentifier, "RSDBI",
                "ReadScalingDataByIdentifier", "讀取縮放資料識別碼",
                DiagnosticSessionMask.Extended, UdsServiceCapability.DataTransmission),

            [UdsService.ReadDataByPeriodicIdentifier] = new(UdsService.ReadDataByPeriodicIdentifier, "RDBPI",
                "ReadDataByPeriodicIdentifier", "週期性讀取識別碼",
                DiagnosticSessionMask.Extended, UdsServiceCapability.DataTransmission),

            [UdsService.DynamicallyDefineDataIdentifier] = new(UdsService.DynamicallyDefineDataIdentifier, "DDDI",
                "DynamicallyDefineDataIdentifier", "動態定義資料識別碼",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.DataTransmission | UdsServiceCapability.HasSubFunction),

            [UdsService.WriteDataByIdentifier] = new(UdsService.WriteDataByIdentifier, "WDBI",
                "WriteDataByIdentifier", "寫入資料識別碼",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.DataTransmission),

            [UdsService.WriteMemoryByAddress] = new(UdsService.WriteMemoryByAddress, "WMBA",
                "WriteMemoryByAddress", "寫入記憶體位址",
                DiagnosticSessionMask.Programming, UdsServiceCapability.DataTransmission),

            // --- Stored Data
            [UdsService.ClearDiagnosticInformation] = new(UdsService.ClearDiagnosticInformation, "CDTCI",
                "ClearDiagnosticInformation", "清除診斷資訊",
                DiagnosticSessionMask.Default | DiagnosticSessionMask.Extended, UdsServiceCapability.StoredData),

            [UdsService.ReadDTCInformation] = new(UdsService.ReadDTCInformation, "RDTCI",
                "ReadDTCInformation", "讀取 DTC 資訊",
                DiagnosticSessionMask.Default | DiagnosticSessionMask.Extended, UdsServiceCapability.StoredData | UdsServiceCapability.HasSubFunction),

            // --- I/O & Routine
            [UdsService.InputOutputControlByIdentifier] = new(UdsService.InputOutputControlByIdentifier, "IOCBI",
                "InputOutputControlByIdentifier", "I/O 控制",
                DiagnosticSessionMask.Extended, UdsServiceCapability.IoControl),

            [UdsService.RoutineControl] = new(UdsService.RoutineControl, "RC",
                "RoutineControl", "例程控制",
                DiagnosticSessionMask.Extended | DiagnosticSessionMask.Programming, UdsServiceCapability.Routine | UdsServiceCapability.HasSubFunction),

            // --- Download / Upload
            [UdsService.RequestDownload] = new(UdsService.RequestDownload, "RD",
                "RequestDownload", "請求下載",
                DiagnosticSessionMask.Programming, UdsServiceCapability.DownloadUpload | UdsServiceCapability.HasSubFunction),

            [UdsService.RequestUpload] = new(UdsService.RequestUpload, "RU",
                "RequestUpload", "請求上傳",
                DiagnosticSessionMask.Programming, UdsServiceCapability.DownloadUpload | UdsServiceCapability.HasSubFunction),

            [UdsService.TransferData] = new(UdsService.TransferData, "TD",
                "TransferData", "資料傳輸",
                DiagnosticSessionMask.Programming, UdsServiceCapability.DownloadUpload),

            [UdsService.RequestTransferExit] = new(UdsService.RequestTransferExit, "RTSE",
                "RequestTransferExit", "結束傳輸",
                DiagnosticSessionMask.Programming, UdsServiceCapability.DownloadUpload | UdsServiceCapability.HasSubFunction),
        };

        public static bool TryGetInfo(UdsService sid, out UdsServiceInfo info) => _db.TryGetValue(sid, out info);

        public static UdsServiceInfo Get(UdsService sid) => _db[sid];

        public static bool IsAllowedIn(this UdsService sid, DiagnosticSessionType s)
            => _db.TryGetValue(sid, out var i) && (i.AllowedSessions & s.ToMask()) != 0;

        public static DiagnosticSessionMask ToMask(this DiagnosticSessionType s) => s switch
        {
            DiagnosticSessionType.DefaultSession => DiagnosticSessionMask.Default,
            DiagnosticSessionType.ProgrammingSession => DiagnosticSessionMask.Programming,
            DiagnosticSessionType.ExtendedSession => DiagnosticSessionMask.Extended,
            _ => DiagnosticSessionMask.None
        };

        public static byte PositiveResponseSid(this UdsService sid) => (byte)((byte)sid + 0x40);

        public static bool Has(this UdsService sid, UdsServiceCapability cap)
            => _db.TryGetValue(sid, out var i) && (i.Capabilities & cap) != 0;

        public static string Mnemonic(this UdsService sid) => _db[sid].Mnemonic;
        public static string EnglishName(this UdsService sid) => _db[sid].English;
        public static string DisplayName(this UdsService sid) => _db[sid].Chinese;
        public static DiagnosticSessionMask AllowedSessions(this UdsService sid) => _db[sid].AllowedSessions;
        public static UdsServiceCapability Capabilities(this UdsService sid) => _db[sid].Capabilities;
    }
}
