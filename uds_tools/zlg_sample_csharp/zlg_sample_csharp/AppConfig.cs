using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    public class AppConfig
    {
        [JsonPropertyName("device_type")]
        public string DeviceType { get; set; } = "ZCAN_USBCANFD_100U";

        [JsonPropertyName("device_index")]
        public uint DeviceIndex { get; set; } = 0;

        [JsonPropertyName("channel_index")]
        public uint ChannelIndex { get; set; } = 0;

        [JsonPropertyName("arb_bps")]
        public uint ArbBps { get; set; } = 104286;

        [JsonPropertyName("data_bps")]
        public uint DataBps { get; set; } = 4260362;

        [JsonPropertyName("tx_id")]
        public string TxId { get; set; } = "682";

        [JsonPropertyName("rx_id")]
        public string RxId { get; set; } = "602";

        [JsonPropertyName("hex_dir")]
        public string HexDir { get; set; } = "";
        
        [JsonPropertyName("command_type")]
        [JsonConverter(typeof(JsonEnumMemberConverter<UDSCommandType>))]
        public UDSCommandType CommandType { get; set; } = UDSCommandType.COMMAND_SNIFFER;

        [JsonPropertyName("sniffer")]
        public SnifferConfig Sniffer { get; set; } = new SnifferConfig();

        [JsonPropertyName("flash")]
        public FlashConfig Flash { get; set; } = new FlashConfig();

        public static AppConfig Load(string path = "config.json")
        {
            if (!File.Exists(path)) return new AppConfig();
            try
            {
                var json = File.ReadAllText(path);
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var cfg = JsonSerializer.Deserialize<AppConfig>(json, options);
                return cfg ?? new AppConfig();
            }
            catch
            {
                return new AppConfig();
            }
        }
    }

    public class FlashConfig
    {
        [JsonPropertyName("aes")]
        public Dictionary<string, List<string>> Aes { get; set; } = new Dictionary<string, List<string>>
        {
            { "1", new List<string> { "0x40", "0xAF", "0x1D", "0x0C", "0x09", "0x97", "0xF9", "0x31", "0x48", "0xF5", "0xB3", "0x65", "0x75", "0xA3", "0x76", "0x1E" } },
            { "2", new List<string> { "0x0D", "0x37", "0x4F", "0x3C", "0xC6", "0x91", "0xD3", "0x4B", "0x91", "0x07", "0xF0", "0x78", "0xA6", "0x4E", "0x75", "0x6B" } }
        };

        public byte[] GetAesKey(int level)
        {
            if (Aes.TryGetValue(level.ToString(), out var hexList))
            {
                byte[] key = new byte[16];
                for (int i = 0; i < Math.Min(16, hexList.Count); i++)
                {
                    string s = hexList[i].Replace("0x", "");
                    key[i] = byte.Parse(s, NumberStyles.HexNumber);
                }
                return key;
            }
            return null;
        }
    }

    public class SnifferConfig
    {
        [JsonPropertyName("commands")]
        public List<UdsCommandConfig> Commands { get; set; } = new List<UdsCommandConfig>();

        [JsonPropertyName("sniffer_log_file")]
        public string SnifferLogFile { get; set; } = "sniffer.log";

        [JsonPropertyName("sniffer_in_new_window")]
        public bool SnifferInNewWindow { get; set; } = false;
    }
}