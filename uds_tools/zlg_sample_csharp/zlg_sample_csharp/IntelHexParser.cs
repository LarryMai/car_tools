using System.Globalization;

namespace zlg_sample_csharp
{
    public class IntelHexSegment
    {
        public uint StartAddress { get; set; }
        public byte[] Data { get; set; } = Array.Empty<byte>();
    }

    public class IntelHexParser
    {
        public static List<IntelHexSegment> Parse(string filePath)
        {
            var segments = new List<IntelHexSegment>();
            uint upperAddress = 0;
            uint currentSegmentAddress = 0;
            var currentData = new List<byte>();

            foreach (var line in File.ReadLines(filePath))
            {
                if (string.IsNullOrWhiteSpace(line) || !line.StartsWith(":")) continue;

                byte byteCount = byte.Parse(line.Substring(1, 2), NumberStyles.HexNumber);
                ushort address = ushort.Parse(line.Substring(3, 4), NumberStyles.HexNumber);
                byte recordType = byte.Parse(line.Substring(7, 2), NumberStyles.HexNumber);
                string dataHex = line.Substring(9, byteCount * 2);

                if (recordType == 0x00) // Data Record
                {
                    uint absoluteAddress = upperAddress | address;
                    if (currentData.Count > 0 && absoluteAddress != currentSegmentAddress + currentData.Count)
                    {
                        // New segment detected (discontinuity)
                        segments.Add(new IntelHexSegment { StartAddress = currentSegmentAddress, Data = currentData.ToArray() });
                        currentData.Clear();
                        currentSegmentAddress = absoluteAddress;
                    }
                    else if (currentData.Count == 0)
                    {
                        currentSegmentAddress = absoluteAddress;
                    }

                    for (int i = 0; i < byteCount; i++)
                    {
                        currentData.Add(byte.Parse(dataHex.Substring(i * 2, 2), NumberStyles.HexNumber));
                    }
                }
                else if (recordType == 0x01) // End Of File
                {
                    if (currentData.Count > 0)
                    {
                        segments.Add(new IntelHexSegment { StartAddress = currentSegmentAddress, Data = currentData.ToArray() });
                        currentData.Clear();
                    }
                    break;
                }
                else if (recordType == 0x02) // Extended Segment Address
                {
                    upperAddress = (uint)ushort.Parse(dataHex, NumberStyles.HexNumber) << 4;
                }
                else if (recordType == 0x04) // Extended Linear Address
                {
                    upperAddress = (uint)ushort.Parse(dataHex, NumberStyles.HexNumber) << 16;
                }
            }

            return segments;
        }
    }
}
