using System.Text.Json.Serialization;

namespace zlg_sample_csharp.Enums
{
    public enum UdsCommandRunType
    {
        [JsonPropertyName("one_shot")]
        OneShot,

        [JsonPropertyName("periodically")]
        Periodically
    }
}
