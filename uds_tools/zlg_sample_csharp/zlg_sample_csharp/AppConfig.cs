using System;
using System.Collections.Generic;
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
        [JsonConverter(typeof(UdsCommandTypeConverter))]
        public UDSCommandType CommandType { get; set; } = UDSCommandType.COMMAND_SNIFFER;

        [JsonPropertyName("commands")]
        public List<UdsCommandConfig> Commands { get; set; } = new List<UdsCommandConfig>();

        [JsonPropertyName("sniffer_log_file")]
        public string SnifferLogFile { get; set; } = "sniffer.log";

        [JsonPropertyName("sniffer_in_new_window")]
        public bool SnifferInNewWindow { get; set; } = false;

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
}