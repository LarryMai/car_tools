using System.Security.Cryptography;

namespace zlg_sample_csharp
{
    public class SecurityAlgorithm
    {
        public byte[] AesKeyLevel1 { get; set; } = new byte[]
        {
            0x40, 0xAF, 0x1D, 0x0C, 0x09, 0x97, 0xF9, 0x31,
            0x48, 0xF5, 0xB3, 0x65, 0x75, 0xA3, 0x76, 0x1E
        };

        public byte[] AesKeyLevel2 { get; set; } = new byte[]
        {
            0x0D, 0x37, 0x4F, 0x3C, 0xC6, 0x91, 0xD3, 0x4B,
            0x91, 0x07, 0xF0, 0x78, 0xA6, 0x4E, 0x75, 0x6B
        };

        public byte[] GenerateKey(byte[] seed, int level = 1)
        {
            byte[] aesKey = level == 2 ? AesKeyLevel2 : AesKeyLevel1;

            using (Aes aes = Aes.Create())
            {
                aes.Key = aesKey;
                aes.Mode = CipherMode.ECB;
                aes.Padding = PaddingMode.None;

                // Python code uses decryptor
                using (ICryptoTransform decryptor = aes.CreateDecryptor())
                {
                    byte[] input = seed;
                    if (seed.Length != 16)
                    {
                        input = new byte[16];
                        Array.Copy(seed, 0, input, 0, Math.Min(seed.Length, 16));
                    }

                    byte[] output = new byte[16];
                    decryptor.TransformBlock(input, 0, 16, output, 0);
                    return output;
                }
            }
        }
    }
}
