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

    public static class UdsServiceExtensions
    {
        public static byte PositiveResponseSid(this UdsService sid)
            => (byte)((byte)sid + 0x40);

        public static string Mnemonic(this UdsService sid) => sid switch
        {
            UdsService.DiagnosticSessionControl => "DSC",
            UdsService.ECUReset => "ER",
            UdsService.SecurityAccess => "SA",
            UdsService.CommunicationControl => "CC",
            UdsService.TesterPresent => "TP",
            UdsService.AccessTimingParameter => "ATP",
            UdsService.SecuredDataTransmission => "SDT",
            UdsService.ControlDTCSetting => "CDTCS",
            UdsService.ResponseOnEvent => "ROE",
            UdsService.LinkControl => "LC",
            UdsService.ReadDataByIdentifier => "RDBI",
            UdsService.ReadMemoryByAddress => "RMBA",
            UdsService.ReadScalingDataByIdentifier => "RSDBI",
            UdsService.ReadDataByPeriodicIdentifier => "RDBPI",
            UdsService.DynamicallyDefineDataIdentifier => "DDDI",
            UdsService.WriteDataByIdentifier => "WDBI",
            UdsService.WriteMemoryByAddress => "WMBA",
            UdsService.ClearDiagnosticInformation => "CDTCI",
            UdsService.ReadDTCInformation => "RDTCI",
            UdsService.InputOutputControlByIdentifier => "IOCBI",
            UdsService.RoutineControl => "RC",
            UdsService.RequestDownload => "RD",
            UdsService.RequestUpload => "RU",
            UdsService.TransferData => "TD",
            UdsService.RequestTransferExit => "RTSE",
            _ => sid.ToString()
        };

        public static string EnglishName(this UdsService sid) => sid switch
        {
            UdsService.DiagnosticSessionControl => "DiagnosticSessionControl",
            UdsService.ECUReset => "ECUReset",
            UdsService.SecurityAccess => "SecurityAccess",
            UdsService.CommunicationControl => "CommunicationControl",
            UdsService.TesterPresent => "TesterPresent",
            UdsService.AccessTimingParameter => "AccessTimingParameter",
            UdsService.SecuredDataTransmission => "SecuredDataTransmission",
            UdsService.ControlDTCSetting => "ControlDTCSetting",
            UdsService.ResponseOnEvent => "ResponseOnEvent",
            UdsService.LinkControl => "LinkControl",
            UdsService.ReadDataByIdentifier => "ReadDataByIdentifier",
            UdsService.ReadMemoryByAddress => "ReadMemoryByAddress",
            UdsService.ReadScalingDataByIdentifier => "ReadScalingDataByIdentifier",
            UdsService.ReadDataByPeriodicIdentifier => "ReadDataByPeriodicIdentifier",
            UdsService.DynamicallyDefineDataIdentifier => "DynamicallyDefineDataIdentifier",
            UdsService.WriteDataByIdentifier => "WriteDataByIdentifier",
            UdsService.WriteMemoryByAddress => "WriteMemoryByAddress",
            UdsService.ClearDiagnosticInformation => "ClearDiagnosticInformation",
            UdsService.ReadDTCInformation => "ReadDTCInformation",
            UdsService.InputOutputControlByIdentifier => "InputOutputControlByIdentifier",
            UdsService.RoutineControl => "RoutineControl",
            UdsService.RequestDownload => "RequestDownload",
            UdsService.RequestUpload => "RequestUpload",
            UdsService.TransferData => "TransferData",
            UdsService.RequestTransferExit => "RequestTransferExit",
            _ => sid.ToString()
        };

        public static string DisplayName(this UdsService sid) => sid switch
        {
            UdsService.DiagnosticSessionControl => "診斷會談控制",
            UdsService.ECUReset => "ECU 重置",
            UdsService.SecurityAccess => "安全存取",
            UdsService.CommunicationControl => "通訊控制",
            UdsService.TesterPresent => "測試器在線",
            UdsService.AccessTimingParameter => "時序參數存取",
            UdsService.SecuredDataTransmission => "安全資料傳輸",
            UdsService.ControlDTCSetting => "DTC 控制設定",
            UdsService.ResponseOnEvent => "事件回應",
            UdsService.LinkControl => "連結控制",
            UdsService.ReadDataByIdentifier => "讀取資料識別碼",
            UdsService.ReadMemoryByAddress => "讀取記憶體位址",
            UdsService.ReadScalingDataByIdentifier => "讀取縮放資料識別碼",
            UdsService.ReadDataByPeriodicIdentifier => "週期性讀取識別碼",
            UdsService.DynamicallyDefineDataIdentifier => "動態定義資料識別碼",
            UdsService.WriteDataByIdentifier => "寫入資料識別碼",
            UdsService.WriteMemoryByAddress => "寫入記憶體位址",
            UdsService.ClearDiagnosticInformation => "清除診斷資訊",
            UdsService.ReadDTCInformation => "讀取 DTC 資訊",
            UdsService.InputOutputControlByIdentifier => "I/O 控制",
            UdsService.RoutineControl => "例程控制",
            UdsService.RequestDownload => "請求下載",
            UdsService.RequestUpload => "請求上傳",
            UdsService.TransferData => "資料傳輸",
            UdsService.RequestTransferExit => "結束傳輸",
            _ => sid.ToString()
        };
    }
}
