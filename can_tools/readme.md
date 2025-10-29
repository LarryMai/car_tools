# 🧮 CAN Tools — Auto CAN Message Generator

這個模組提供 **由 DBC 自動產生 CAN FD 訊息編碼／解碼的 Python 程式**。
給定一份 `.dbc` 檔，它會輸出可直接使用的 `generate_0x<ID>.py`，內含資料結構、Enum、編碼和解碼函式與測試樣例。

---

## 🚗 Overview

`auto_generate_can_msg.py` 會讀取你的 DBC，產生一支 Python 腳本（例如 `generate_0x495.py`），內容包括：

* `@dataclass` 訊息結構（欄位自動帶入對應的 `IntEnum` 或 `int`）
* `generate_0x<ID>_can_msg_bytes()` 編碼（**回傳 ******``******，更易除錯與檢視**）
* `decode_0x<ID>_can_msg()` 解碼
* 位元階（byte/bit）除錯列印
* 具「**可拷貝貼上**」的完整建構子示例（所有欄位一覽，Enum 預設值註解）
* 內建 `STRICT_ENUM` 與 `to_enum()`：支援 **寬鬆／嚴格** Enum 模式

> 舊版 README 範例與基本操作沿用並擴充（如下文）。

---

## ⚙️ Installation

```
pip install cantools

```

---

## 🧬 CLI 使用方式

```
python auto_generate_can_msg.py --dbc <DBC_FILE_PATH> --id <CAN_ID|all> [--out <DIR>] [--prefix <STR>] [--debug] [--list] [--strict]

```

### 參數一覽

| 參數 說明      |                                                                   |
| ---------- | ----------------------------------------------------------------- |
| `--dbc`    | DBC 檔路徑（例如：`./dbcs/meter/FPD1_102_4_CAN2_Meter_20250805_Fix.dbc`） |
| `--id`     | 目標 CAN ID（`0x495` 或 `1173`）；或輸入 `all` 產生所有訊息                      |
| `--out`    | 輸出目錄（預設 `.`）                                                      |
| `--prefix` | 產出檔名前綴（例如 `--prefix IVI_` 會產生 `IVI_generate_0x*.py`）              |
| `--debug`  | 開啟 bit 級除錯列印（編碼／解碼時顯示 byte/bit 設定位元）                              |
| `--list`   | 僅列出 DBC 中的所有訊息與訊號（不輸出檔案）                                          |
| `--strict` | 嚴格 Enum 模式（解碼遇到未知值直接拋錯；預設為**寬鬆**）                                 |

---

## 🥪 Example 1：輸出單一 CAN 模組

```
python auto_generate_can_msg.py --dbc <your.dbc> --id 0x495

```

這會在輸出目錄建立：

```
generate_0x495.py

```

> 舊版說明亦包含產生單支檔案的說明，沿用不變。

---

## 🧰 Example 2：產生全部訊息（加上前綴）與嚴格 Enum

```
python auto_generate_can_msg.py --dbc ./dbcs/meter/FPD1_102_4_CAN2_Meter_20250805_Fix.dbc --id all --prefix IVI_ --strict

```

* 會為 DBC 內每個訊息輸出 `IVI_generate_0x<ID>.py`
* 嚴格模式下，解碼遇到未定義的枚舉值會直接拋出例外

---

## 📜 Example 3：列出 DBC 內容

```
python auto_generate_can_msg.py --dbc ./dbcs/meter/FPD1_102_4_CAN2_Meter_20250805_Fix.dbc --list

```

輸出包含每個 message 的 ID / DLC 與每個 signal 的 bit 範圍、位元序（big_endian / little_endian）。

---

## ▶️ Example 4：執行產生的模組

產生 `generate_0x<ID>.py` 後，直接執行即可看到 **編碼（list 與 hex）→ 解碼** 的來回測試：

```
python generate_0x<ID>.py

```

典型輸出會有：

* `[DEBUG] Encoded data list: [...]`
* `[DEBUG] Encoded data bytes: 00:00:...`
* `Decoded message: canfd_0x<ID>_msg(...)`

> 舊版 README 也示範了執行與輸出樣貌。

---

## ✨ 產生檔的結構（重點）

每支 `generate_0x<ID>.py` 內包含：

* `get_motorola_bit_positions()`：**Motorola（big-endian）** 位元映射小工具
* 常數：每個 Signal 的 `_OFFSET / _LEN / _BYTE_ORDER`
* `@dataclass canfd_0x<ID>_msg`：欄位型別自動選用 `IntEnum` 或 `int`
* `generate_0x<ID>_can_msg_bytes(msg, debug=False) -> List[int]`：**回傳 **``（好除錯，再用 `bytes(list)` 可得位元組）
* `decode_0x<ID>_can_msg(data: bytes, debug=False) -> canfd_0x<ID>_msg`
* **完整建構子範例**（所有欄位一覽、Enum 預設值註解），方便 copy-paste
* `STRICT_ENUM` 與 `to_enum()`：解碼時套用 **嚴格／寬鬆** 模式

> 舊版有簡表，現已補齊最新功能（回傳 `List[int]`、建構子清單、嚴格模式等）。

---

## 🧠 Enum 與值處理

* 會從 DBC 的 value descriptions 產生對應 `IntEnum` 類別。
* 會自動把 enum 標籤清理成 `SCREAMING_SNAKE_CASE`，避免非法識別字。
* 對於 DBC 中標記為 `Not used` 的條目，會輸出為連續的 `RESERVED_1 / RESERVED_2 / ...`，避免重名衝突。
* 產生檔內含：

  ```
  STRICT_ENUM = False  # 預設寬鬆
  def to_enum(cls, value, strict=False):
      try:
          return cls(int(value))
      except Exception:
          if strict:
              raise
          return int(value)

  ```

  * **寬鬆模式**：未知枚舉值 → 保留原始 `int`，不中斷流程
  * **嚴格模式**：未知枚舉值 → 直接拋錯，便於驗證資料品質

---

## 🔎 Debug 輸出（位元級）

啟用 `--debug`（或在程式內 `debug=True`），編碼／解碼會列印：

```
Encode <Signal>: byte[b] bit[k] → 0x.. → 0x..
Decode <Signal>: byte=b, bit=k, val=1
[DEBUG] Encoded data list: [...]
[DEBUG] Encoded data bytes: 00:00:...

```

對校對實機／產線流程非常實用。

---

## 📂 建議專案結構

```
car_tools/
│
├── can_tools/
│   ├── auto_generate_can_msg.py      ← 產生器
│   ├── generate_0xID.py             ← 產生出的 CAN FD 模組
│   └── README.md

```

> 舊版也有此區塊，保留並微調說明。

---

## 🧩 已知相容性與注意事項

* 同時支援 **Motorola (big_endian)** 與 **Intel (little_endian)** 位元序。
* CAN FD 最長 64 bytes。
* 產生檔預設回傳 `List[int]`，若需 `bytes` 請自行 `bytes(list_int)`。
* 產生的 `__main__` 範例使用 **明確建構子列出所有欄位**，對同事「看得見能設哪些欄位」很友善。

---

## 🧾 License

MIT License © 2025 [LarryMai](https://github.com/LarryMai)

---

