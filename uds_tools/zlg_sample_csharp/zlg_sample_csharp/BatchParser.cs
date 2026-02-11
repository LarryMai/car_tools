using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace zlg_sample_csharp
{
    public class BatchCommand
    {
        public uint Address { get; set; }
        public string FilePath { get; set; } = "";
    }

    public static class BatchParser
    {
        public static List<BatchCommand> Parse(string batPath)
        {
            var commands = new List<BatchCommand>();
            var variables = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            
            string batDir = Path.GetDirectoryName(Path.GetFullPath(batPath)) ?? "";
            
            // Standard variables from the bat file
            variables["COM_PORT"] = "COM1"; 
            variables["BAUD_RATE"] = "921600";

            string[] lines = File.ReadAllLines(batPath);

            // Regex for 'set VAR=VALUE'
            var setRegex = new Regex(@"^\s*set\s+([A-Za-z0-9_]+)=(.+)$", RegexOptions.IgnoreCase);
            
            // Regex for 'WriteFlash %COM_PORT% %BAUD_RATE% 0xADDRESS FILEPATH'
            // We ignore the first few parameters and focus on address and path
            var writeRegex = new Regex(@"WriteFlash\s+\S+\s+\S+\s+(0x[0-9A-Fa-f]+)\s+(.+)$", RegexOptions.IgnoreCase);

            foreach (var line in lines)
            {
                string trimmed = line.Trim();
                if (trimmed.StartsWith("::") || trimmed.StartsWith("REM", StringComparison.OrdinalIgnoreCase)) continue;

                var setMatch = setRegex.Match(trimmed);
                if (setMatch.Success)
                {
                    string key = setMatch.Groups[1].Value;
                    string value = setMatch.Groups[2].Value.Trim('"', '\'');
                    variables[key] = value;
                    continue;
                }

                var writeMatch = writeRegex.Match(trimmed);
                if (writeMatch.Success)
                {
                    string addrStr = writeMatch.Groups[1].Value.Replace("0x", "");
                    uint address = uint.Parse(addrStr, System.Globalization.NumberStyles.HexNumber);
                    string rawPath = writeMatch.Groups[2].Value.Trim('"', '\'');

                    // Resolve variables %VAR%
                    foreach (var kvp in variables)
                    {
                        rawPath = rawPath.Replace($"%{kvp.Key}%", kvp.Value);
                    }

                    // Resolve relative paths based on bat location
                    string fullPath = Path.IsPathRooted(rawPath) 
                        ? rawPath 
                        : Path.GetFullPath(Path.Combine(batDir, rawPath));

                    commands.Add(new BatchCommand { Address = address, FilePath = fullPath });
                }
            }

            return commands;
        }
    }
}