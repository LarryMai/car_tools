using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Xml;

namespace zlg_sample_csharp
{
    public static class ZFlashGenerator
    {
        public static void Generate(string outputPath, IEnumerable<string> hexFiles, string txId = "682", string rxId = "602")
        {
            // Register encoding provider for GB2312
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            Encoding gb2312 = Encoding.GetEncoding("GB2312");

            XmlWriterSettings settings = new XmlWriterSettings
            {
                Encoding = gb2312,
                Indent = true,
                IndentChars = "  ",
                NewLineChars = "\n",
                OmitXmlDeclaration = false
            };

            using (XmlWriter writer = XmlWriter.Create(outputPath, settings))
            {
                writer.WriteStartDocument();
                writer.WriteComment("Created By ZLG ZCANPRO (Modified by Gemini CLI)");
                writer.WriteStartElement("flow");

                // 1. Setting Item
                WriteSettingItem(writer, txId, rxId);

                // 2. Extended Session (General Item)
                WriteGeneralItem(writer, "10", "進入擴展模式", "03 ");

                // 3. Security Access (Security Item)
                WriteSecurityItem(writer);

                // 4. Control DTC (General Item)
                WriteGeneralItem(writer, "85", "關閉DTC記錄", "02 ");

                // 5. Communication Control (General Item)
                WriteGeneralItem(writer, "28", "關閉非診斷通訊", "03 03 ");

                // 6. Download Items
                foreach (var hexFile in hexFiles)
                {
                    WriteDownloadItem(writer, hexFile, outputPath);
                }

                // 7. ECU Reset (General Item)
                WriteGeneralItem(writer, "11", "ECU重置", "03 ");

                writer.WriteEndElement(); // flow
                writer.WriteEndDocument();
            }
        }

        private static void WriteSettingItem(XmlWriter writer, string txId, string rxId)
        {
            writer.WriteStartElement("item");
            writer.WriteAttributeString("type", "setting");

            var settings = new Dictionary<string, string>
            {
                {"src_addr", "700"},
                {"dst_addr", rxId},
                {"fun_addr", "7d0"},
                {"phy_addr", txId},
                {"comm_frame_type", "0"},
                {"session_keep_suppress_response", "1"},
                {"session_keep_enable", "0"},
                {"session_keep_addr", "7d0"},
                {"timeout", "2000"},
                {"neg78_timeout", "5000"},
                {"local_st_min", "0"},
                {"remote_st_min", "0"},
                {"is_modify_ecu_stmin", "0"},
                {"file_block_interval", "0"},
                {"file_block_retry", "2"},
                {"block_size", "0"},
                {"version", "1"},
                {"is_fill_byte", "1"},
                {"fill_byte", "204"},
                {"fc_timeout", "1000"},
                {"session_keep_interval", "2000"},
                {"show_session_keep_info", "0"},
                {"show_raw_frame", "1"},
                {"output_max_row_count", "100000"},
                {"single_file_max_row_count", "100000"},
                {"can_type", "2"},
                {"check_any_negative_response", "0"},
                {"wait_if_suppress_response", "0"}
            };

            foreach (var kvp in settings)
            {
                writer.WriteElementString(kvp.Key, kvp.Value);
            }
            writer.WriteElementString("lib_path", "");
            writer.WriteEndElement();
        }

        private static void WriteGeneralItem(XmlWriter writer, string sid, string desc, string data)
        {
            writer.WriteStartElement("item");
            writer.WriteAttributeString("type", "general");
            writer.WriteElementString("functionaddr", "false");
            writer.WriteElementString("is_crc_cmd", "false");
            writer.WriteElementString("sid", sid);
            writer.WriteElementString("desc", desc);
            writer.WriteElementString("data", data);
            writer.WriteElementString("suppress_response", "false");
            writer.WriteEndElement();
        }

        private static void WriteSecurityItem(XmlWriter writer)
        {
            writer.WriteStartElement("item");
            writer.WriteAttributeString("type", "security");
            writer.WriteElementString("functionaddr", "false");
            writer.WriteElementString("level", "1");
            writer.WriteElementString("dll", "sa_demo_fox_v0.0.2.dll");
            writer.WriteElementString("desc", "安全訪問");
            writer.WriteElementString("ignore_unlocked_check", "false");
            writer.WriteEndElement();
        }

        private static void WriteDownloadItem(XmlWriter writer, string hexFile, string zflashPath)
        {
            writer.WriteStartElement("item");
            writer.WriteAttributeString("type", "download");
            
            string relPath = hexFile;
            try
            {
                Uri hexUri = new Uri(Path.GetFullPath(hexFile));
                Uri zflashUri = new Uri(Path.GetFullPath(zflashPath));
                relPath = Uri.UnescapeDataString(zflashUri.MakeRelativeUri(hexUri).ToString()).Replace('/', '\\');
            }
            catch {}

            writer.WriteElementString("desc", Path.GetFileNameWithoutExtension(hexFile));
            writer.WriteElementString("functionaddr", "false");
            writer.WriteElementString("file", relPath);
            writer.WriteElementString("dataFormatIdentifier", "2");
            writer.WriteElementString("addresssize", "4");
            writer.WriteElementString("lengthsize", "4");
            writer.WriteElementString("erase_ecu_memory_mode", "3");
            writer.WriteElementString("crc_type", "0");
            writer.WriteElementString("crc_poly", "4c11db7");
            writer.WriteElementString("crc_init_value", "ffffffff");
            writer.WriteElementString("crc_xor_value", "ffffffff");
            writer.WriteElementString("crc_in_reverse", "1");
            writer.WriteElementString("crc_out_reverse", "1");
            writer.WriteElementString("crc_cmd", "31 01 02 02 ");
            writer.WriteElementString("crc_enable", "0");
            writer.WriteElementString("crc_block_enable", "1");
            writer.WriteElementString("customParamForS37Enable", "0");
            writer.WriteElementString("file_blocks_enable", "0,1");
            writer.WriteElementString("ever_file_block_delay", "0");
            writer.WriteElementString("crc_block_custom_enable", "0");
            writer.WriteElementString("crc_block_custom_cmd", "31 01 F1 A0 ");
            writer.WriteElementString("customParamForS37", "");
            writer.WriteEndElement();
        }
    }
}
