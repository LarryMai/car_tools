using System;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace zlg_sample_csharp.Enums
{
    public class JsonEnumMemberConverter<T> : JsonConverter<T> where T : struct, Enum
    {
        public override T Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            string? enumString = reader.GetString();
            if (string.IsNullOrEmpty(enumString))
            {
                return default;
            }

            foreach (var field in typeof(T).GetFields())
            {
                var attribute = field.GetCustomAttribute<JsonPropertyNameAttribute>();
                if (attribute != null && string.Equals(attribute.Name, enumString, StringComparison.OrdinalIgnoreCase))
                {
                    return (T)field.GetValue(null)!;
                }

                if (string.Equals(field.Name, enumString, StringComparison.OrdinalIgnoreCase))
                {
                    return (T)field.GetValue(null)!;
                }
            }

            if (Enum.TryParse(enumString, true, out T result))
            {
                return result;
            }

            return default;
        }

        public override void Write(Utf8JsonWriter writer, T value, JsonSerializerOptions options)
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
