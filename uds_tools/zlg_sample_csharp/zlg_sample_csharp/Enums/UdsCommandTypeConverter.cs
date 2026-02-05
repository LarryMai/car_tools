using System;
using System.Linq;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace zlg_sample_csharp.Enums
{
    public class UdsCommandTypeConverter : JsonConverter<UDSCommandType>
    {
        public override UDSCommandType Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            string? enumString = reader.GetString();
            if (string.IsNullOrEmpty(enumString))
            {
                return UDSCommandType.COMMAND_UNKNOWN;
            }

            foreach (var field in typeToConvert.GetFields())
            {
                var attribute = field.GetCustomAttribute<JsonPropertyNameAttribute>();
                if (attribute != null && string.Equals(attribute.Name, enumString, StringComparison.OrdinalIgnoreCase))
                {
                    return (UDSCommandType)field.GetValue(null)!;
                }
                
                // Fallback to checking the enum name itself
                if (string.Equals(field.Name, enumString, StringComparison.OrdinalIgnoreCase))
                {
                    return (UDSCommandType)field.GetValue(null)!;
                }
            }

            // Fallback for integer values if passed as string or number (not expected here but good for safety)
            if (Enum.TryParse(enumString, true, out UDSCommandType result))
            {
                return result;
            }

            throw new JsonException($"Unknown value for UDSCommandType: {enumString}");
        }

        public override void Write(Utf8JsonWriter writer, UDSCommandType value, JsonSerializerOptions options)
        {
            var field = value.GetType().GetField(value.ToString());
            var attribute = field?.GetCustomAttribute<JsonPropertyNameAttribute>();
            if (attribute != null)
            {
                writer.WriteStringValue(attribute.Name);
            }
            else
            {
                writer.WriteStringValue(value.ToString());
            }
        }
    }
}
