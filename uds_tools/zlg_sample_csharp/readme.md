# zlg_sample_csharp

## 1) 環境

* **OS**：Windows 11
* **.NET SDK**：**8.0 以上**（`dotnet --info` 可檢查）
* **Python**：3.8 以上（僅部分工具腳本需要；核心專案用 .NET）
* **ZLG 依賴**：`Reference\CAN_lib.zip`（或執行 `Reference\install_zlg.bat` 把 DLL 複製到輸出資料夾）

---

## 2) Build & Run

在專案根目錄（含 `build.bat` 的資料夾）開啟 **Developer PowerShell / CMD**：

```bat
REM (A) 直接編譯（預設 Debug/x64，輸出到 build\x64）
build.bat

REM (B) 指定組態與架構：
build.bat Release x86
build.bat Release x64

REM 編譯完成後，執行輸出資料夾中的 EXE
build\x64\zlg_sample_csharp.exe
```

> `build.bat` 會使用 `dotnet build` 輸出到 `build\<arch>`；若你有 `Reference\install_zlg.bat`，可在 `build.bat` 內接著呼叫來複製 `zlgcan.dll` 與 `kerneldlls\` 到輸出資料夾。

---

## 3) 指令說明 (CLI Commands)

編譯完成後，可以使用下列子指令執行各項功能：

### A. 批量轉換 (batch-convert) - **NEW**
解析 `.bat` 腳本或掃描目錄，將 `.bin`/`.rle` 檔案批量轉換為 `.hex`，並自動產生 `.zflash` 設定檔。
```powershell
# 使用 .bat 腳本進行轉換
.\zlg_sample_csharp.exe batch-convert --bat "C:\path\to\script.bat" --out_dir "C:\output" --txid 682 --rxid 602

# 直接對目錄下的所有 bin 檔進行轉換 (統一起始位址)
.\zlg_sample_csharp.exe batch-convert --src_dir "C:\bin_files" --addr 0x0 --out_dir "C:\output"
```
*   `--bat`: 輸入包含位址資訊的 `.bat` 腳本路徑。
*   `--src_dir`: 若不使用腳本，直接掃描此目錄下的 `.bin` 或 `.rle` 檔案。
*   `--addr`: 起始位址 (Hex 格式，預設 `0x0`)。
*   `--out_dir`: 輸出目錄。
*   `--txid / --rxid`: 用於生成 `.zflash` 的 CAN ID。

### B. UDS 刷寫 (flash)
讀取目錄下的 HEX 檔案並執行 UDS 刷寫流程。
```powershell
.\zlg_sample_csharp.exe flash --hex_dir "C:\hex_output" --dev_type USBCANFD-200U --can_index 0
```

### C. CAN 監聽 (sniffer)
進入 CAN 總線監聽模式，支援顯示 UDS 解析後的內容。
```powershell
# 監聽並定時讀取 DID 1305
.\zlg_sample_csharp.exe sniffer --txid 682 --rxid 602 --did 1305 --new-window
```

### D. 單一檔案轉換 (convert)
將單一 Binary 檔案轉換為 Hex 格式。
```powershell
.\zlg_sample_csharp.exe convert --bin "firmware.bin" --addr 0x10000 --out_dir ./output
```

---

## 4) 全域參數 (Common Options)
適用於多數硬體通訊相關指令：
*   `--dev_type`: ZLG 裝置型號 (例如: `USBCANFD-200U`, `USBCAN-2E-U`)
*   `--dev_index`: 裝置索引 (預設: `0`)
*   `--can_index`: 通道索引 (預設: `0`)
*   `--arb`: 仲裁位元率 (bps, 預設: `500000`)
*   `--data`: 資料位元率 (FD data phase, 預設: `2000000`)
*   `--txid`: UDS 發送 CAN ID (Hex, 預設: `682`)
*   `--rxid`: UDS 接收 CAN ID (Hex, 預設: `602`)