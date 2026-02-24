namespace zlg_sample_csharp.Enums
{
    public static class UdsConstants
    {
        // Control DTC Setting (0x85)
        public const byte DtcSettingOn = 0x01;
        public const byte DtcSettingOff = 0x02;

        // Communication Control (0x28) - Control Type
        public const byte EnableRxAndTx = 0x00;
        public const byte EnableRxDisableTx = 0x01;
        public const byte DisableRxEnableTx = 0x02;
        public const byte DisableRxAndTx = 0x03;

        // Communication Control (0x28) - Communication Type
        public const byte NormalCommunicationMessages = 0x01;
        public const byte NetworkManagementCommunicationMessages = 0x02;
        public const byte NetworkManagementAndNormalCommunicationMessages = 0x03;

        // ECU Reset (0x11)
        public const byte HardReset = 0x01;
        public const byte KeyOffOnReset = 0x02;
        public const byte SoftReset = 0x03;
        public const byte EnableRapidPowerShutDown = 0x04;
        public const byte DisableRapidPowerShutDown = 0x05;
    }
}
