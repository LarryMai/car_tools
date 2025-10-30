# CAN Sim Server (ZLG) — Examples (Local DLLs Only)

請將 **zlgcan.py / zlgcan.dll / kerneldlls/** 放在 **examples/** 目錄（與 `can_sim_server_zlg.py` 同層）。
本工具不會修改系統 PATH，也不接受其他路徑參數。

## 乾跑（無硬體）

**powershell**命令如下:

```powershell
python3 examples\can_sim_server_zlg.py `
  --dbc-adapter-dir dbc_adapters `
  --id-list 0x117 `
  --dry-run `
  --log-level DEBUG `
  --config examples\sim_config.yamL
```

## 實機（ZLG）

**powershell**命令如下:

```powershell
cd ./examples 

python3 ./can_sim_server_zlg.py `
  --dbc-adapter-dir dbc_adapters `
  --id-list 0x117 `
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 `
  --abit 500000 --dbit 2000000 `
  --config ./sim_config.yaml
```

> 單一 adapter 亦可使用 `--parser-mod dbc_adapters.generator_adapter_0x117`。

## Others

- `tx_tester.py`：定時送 CAN / CAN FD 幀（可設 FD/BRS/Extended/週期/次數）。
- `rx_sniffer.py`：簡易收包印出（可搭配 `tx_tester.py` 對打）。

> 放置規範：`zlgcan.py`、`zlgcan.dll`、`kerneldlls/` 必須與 `can_sim_server_zlg.py` 同層（即 `examples/`）— 程式不會改動系統 PATH。

**快速示例**
發送端（每 500ms 送一包 FD+BRS 擴展幀，無限循環），**powershell**命令如下:

```powershell
python examples\\tx_tester.py ^
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 ^
  --abit 500000 --dbit 2000000 ^
  --id 0x117 --data "11 22 33 44 55 66 77 88 99 AA" ^
  --fd --brs --extended ^
  --period-ms 500 --count 0
```

收包端：

```powershell
python examples\\rx_sniffer.py ^
  --dev-type USBCANFD_100U --dev-idx 0 --chan 0 ^
  --abit 500000 --dbit 2000000
```
