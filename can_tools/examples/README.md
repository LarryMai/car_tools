# CAN Sim Server (ZLG) — Examples (Local DLLs Only)

請將 **zlgcan.py / zlgcan.dll / kerneldlls/** 放在 **examples/** 目錄（與 `can_sim_server_zlg.py` 同層）。
本工具不會修改系統 PATH，也不接受其他路徑參數。

## 乾跑（無硬體）

```powershell
python3 examples\can_sim_server_zlg.py `
  --dbc-adapter-dir dbc_adapters `
  --id-list 0x117 `
  --dry-run `
  --log-level DEBUG `
  --config examples\sim_config.yamL
```

## 實機（ZLG）

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
