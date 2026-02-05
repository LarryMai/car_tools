using System.ComponentModel;
using System.Text.Json.Serialization;

namespace zlg_sample_csharp.Enums
{
    public enum UDSCommandType
    {
        [Description("none")]
        [JsonPropertyName("none")]
        COMMAND_UNKNOWN = 0,
        
        [Description("sniffer")]
        [JsonPropertyName("sniffer")]
        COMMAND_SNIFFER = 1,
        
        [Description("flash")]
        [JsonPropertyName("flash")]
        COMMAND_UDS_FLASH = 2
    }
}