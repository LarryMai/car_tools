using System.Text.Json.Serialization;

namespace zlg_sample_csharp
{
    public class UdsCommandConfig
    {
        [JsonPropertyName("type")]
        public string Type { get; set; } = "one_shot"; // default

        [JsonPropertyName("service")]
        public string Service { get; set; } = "";

        [JsonPropertyName("did")]
        public string Did { get; set; } = "";
    }
}
