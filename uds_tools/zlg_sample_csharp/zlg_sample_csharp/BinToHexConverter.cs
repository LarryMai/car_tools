using System;
using System.IO;
using System.Text;

namespace zlg_sample_csharp
{
    public static class BinToHexConverter
    {
        public static void Convert(string binPath, string hexPath, uint baseAddress)
        {
            byte[] data = File.ReadAllBytes(binPath);
            using (StreamWriter sw = new StreamWriter(hexPath))
            {
                uint currentUpperAddress = 0xFFFFFFFF;
                int offset = 0;
                while (offset < data.Length)
                {
                    uint currentAddress = (uint)(baseAddress + offset);
                    uint upperAddress = currentAddress >> 16;

                    if (upperAddress != currentUpperAddress)
                    {
                        // Write Extended Linear Address Record (Type 04)
                        WriteRecord(sw, 0x0000, 0x04, new byte[] { (byte)(upperAddress >> 8), (byte)(upperAddress & 0xFF) });
                        currentUpperAddress = upperAddress;
                    }

                    int lineLen = Math.Min(16, data.Length - offset);
                    // Check if 16-bit address wraps around
                    ushort addr16 = (ushort)(currentAddress & 0xFFFF);
                    if (addr16 + lineLen > 0x10000)
                    {
                        lineLen = 0x10000 - addr16;
                    }

                    byte[] lineData = new byte[lineLen];
                    Array.Copy(data, offset, lineData, 0, lineLen);
                    WriteRecord(sw, addr16, 0x00, lineData);

                    offset += lineLen;
                }

                // Write End of File Record (Type 01)
                WriteRecord(sw, 0x0000, 0x01, Array.Empty<byte>());
            }
        }

        private static void WriteRecord(StreamWriter sw, ushort address, byte type, byte[] data)
        {
            byte len = (byte)data.Length;
            byte checksum = len;
            checksum += (byte)(address >> 8);
            checksum += (byte)(address & 0xFF);
            checksum += type;
            foreach (byte b in data) checksum += b;
            checksum = (byte)((~checksum + 1) & 0xFF);

            string dataHex = data.Length > 0 ? BitConverter.ToString(data).Replace("-", "") : "";
            sw.WriteLine($":{len:X2}{address:X4}{type:X2}{dataHex}{checksum:X2}");
        }
    }
}
