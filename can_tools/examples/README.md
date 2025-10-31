# CAN Sim Server (ZLG) — Examples（Local DLLs Only）

> **放置規範**：請將 `zlgcan.py / zlgcan.dll / kerneldlls/` 放在 **`examples/`** 目錄（與 `can_sim_server_zlg.py` 同層）。程式**不會**修改系統 PATH，也**不接受**其他路徑參數。

## 乾跑（無硬體）

**PowerShell：**

```powershell
python3 examples\can_sim_server_zlg.py `
  --dbc-adapter-dir dbc_adapters `
  --id-list 0x117 `
  --dry-run `
  --log-level DEBUG `
  --config examples\sim_config.yaml
```

> 註：Windows PowerShell 使用反引號 `作為續行；如果用`cmd.exe`請改用`^`，若用 WSL/Bash 請改用 ``。

## 實機（ZLG）

**PowerShell：**

```powershell
cd .\examples

python3 .\can_sim_server_zlg.py `
  --dbc-adapter-dir dbc_adapters `
  --id-list 0x117 `
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 `
  --abit 500000 --dbit 2000000 `
  --config .\sim_config.yaml
```

> 只載入單一 adapter 也可用：
>
> ```c
> --parser-mod dbc_adapters.generator_adapter_0x117
> ```

## 工具（Tx / Rx / 自測）

* `tx_tester.py`：定時送 CAN / CAN FD 幀（支援 FD/BRS/Extended/週期/次數）。
* `rx_sniffer.py`：簡易收包印出（可與 `tx_tester.py` 對打）。
* `txrx_selftest_param_batch.py`：**單通道裝置**的 loopback／TX-echo 自測（支援可調取包批量）。

### 快速示例

發送端（每 500ms 送一包 FD+BRS 擴展幀，無限循環）：

```powershell
python .\examples\tx_tester.py `
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 `
  --abit 500000 --dbit 2000000 `
  --id 0x117 --data "11 22 33 44 55 66 77 88 99 AA" `
  --fd --brs --extended `
  --period-ms 500 --count 0
```

收包端：

```powershell
python .\examples\rx_sniffer.py `
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 `
  --abit 500000 --dbit 2000000
```

單機自我收發（單通道）：

```powershell
python .\examples\txrx_selftest_param_batch.py `
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 `
  --abit 500000 --dbit 2000000 `
  --id 0x117 --data "DE AD BE EF" `
  --fd --brs --period-ms 500 `
  --rx-batch-fd 64 --rx-batch 128
```

> `--rx-batch-fd / --rx-batch` 是**每次呼叫 Receive 取的幀數**（不是 payload 長度）。少量＝低延遲；大量＝高吞吐。

## 注意事項 / 疑難排解

* **通道獨占**：同一通道不能同時被兩個程式 `StartCAN`。若要同時 Tx/Rx，請用**雙通道互連**或第二顆介面，或用上面的自測腳本。
* **位元率／模式一致**：Arb=500k、Data=2M、FD、BRS 必須兩端一致；否則收不到包。
* **終端電阻**：總線兩端各 120Ω；不少 USBCANFD 有內建終端開關，請確認狀態。
* **接地**：兩端需共地（GND）。
* **USBCANFD_100U_MINI**：部分機型/SDK 名稱不同或不支援，若打不開請改用 `USBCANFD_100U/200U/400U/800U`。
* **TX-echo / Loopback**：不同韌體支援度不同。如果只有 `[TX]` 沒 `[RX]`，請改用雙節點測試，或確認 `txrx_selftest_param_batch.py` 的「送完即讀」路徑是否有抓到 echo/loopback 幀。
* **PowerShell 續行**：反引號 `，`cmd.exe`用`^`，Bash 用 ``。

---
