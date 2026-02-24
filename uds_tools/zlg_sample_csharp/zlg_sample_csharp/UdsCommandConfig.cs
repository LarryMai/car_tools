using System.Text.Json.Serialization;
using zlg_sample_csharp.Enums;

namespace zlg_sample_csharp
{
    public class UdsCommandConfig
    {
        [JsonPropertyName("type")]
        [JsonConverter(typeof(JsonEnumMemberConverter<UdsCommandRunType>))]
        public UdsCommandRunType Type { get; set; } = UdsCommandRunType.OneShot; // default

        [JsonPropertyName("service")]
        public string Service { get; set; } = "";

        [JsonPropertyName("did")]
        public string Did { get; set; } = "";
    }
}
