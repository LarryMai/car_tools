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
