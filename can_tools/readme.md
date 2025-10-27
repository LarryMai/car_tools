# 🧮 CAN Tools — Auto CAN Message Generator

This module provides an **automatic CAN message generator and decoder** for Python.
Given a `.dbc` file, it will generate ready-to-use Python code for encoding and decoding CAN FD messages.

📦 Repository: [LarryMai/car_tools](https://github.com/LarryMai/car_tools/tree/main/can_tools)

---

## 🚗 Overview

`auto_generate_can_msg.py` reads your DBC file and produces a Python script (e.g. `generate_0xID.py`)
that contains:

* A structured `@dataclass` message definition
* A `generate_0x<ID>_can_msg_bytes()` encoder function
* A `decode_0x<ID>_can_msg()` decoder function
* Built-in debug and test examples

This greatly simplifies CAN message manipulation for testing and automation pipelines.

---

## ⚙️ Installation

```bash
pip install cantools
```

Optional but recommended:

```bash
pip install tqdm rich
```

---

## 🧬 Basic Usage

```bash
python auto_generate_can_msg.py --dbc <DBC_FILE_PATH> --id <CAN_ID> [options]
```

### Parameters

| Option    | Description                                                                           |
| :-------- | :------------------------------------------------------------------------------------ |
| `--dbc`   | Path to your DBC file. Example: `./dbcs/meter/FPD1_102_4_CAN2_Meter_20250805_Fix.dbc` |
| `--id`    | Target CAN ID (e.g. `0x495` or `1173`)                                                |
| `--out`   | (Optional) Output directory, defaults to current folder                               |
| `--debug` | (Optional) Enable bit-level debug printouts                                           |
| `--list`  | (Optional) List all messages and signals in the DBC file                              |

---

## 🥪 Example 1: Generate a CAN Encoder/Decoder File

```bash
python auto_generate_can_msg.py --dbc <your dbc file path> --id < can msg id>
```

This creates a new file in your working directory:

```
generate_0x495.py
```

---

## 🧰 Example 2: Encode & Decode Test

After generating the file, run it directly:

```bash
python generate_0x<ID>.py
```

Example Output:

```
Encode MFRD_N_Bright_Req: byte[41] bit 6 set → 0x00 → 0x40
Encode MFRD_N_Bright_Req: byte[41] bit 5 set → 0x40 → 0x60
Encode MFRD_N_Bright_Req: byte[41] bit 4 set → 0x60 → 0x70
[DEBUG] Encoded data bytes: 00:00:00:...:64:00:00:00
Decoded message: canfd_0x495_msg(MFRD_N_Bright_Req=100, IVI_IC_Brightness_Sta=100, ...)
```

---

## 📜 Example 3: List DBC Messages

```bash
python auto_generate_can_msg.py --dbc ./dbcs/meter/FPD1_102_4_CAN2_Meter_20250805_Fix.dbc --list
```

Output:

```
Message: FPD1_CAN_Meter, ID: 0x495, DLC: 64
   Signal: MFRD_N_Bright_Req (334..328 bits) order: big_endian
   Signal: IVI_Backlight_Sta (509..509 bits) order: big_endian
   ...
```

---

## 🧱 Generated Code Structure

Each generated Python file includes:

* `get_motorola_bit_positions()` — helper for big-endian bit mapping
* Constant bit offset definitions
* A data class for message definition
* Two main functions:

  * `generate_0x<ID>_can_msg_bytes()`
  * `decode_0x<ID>_can_msg()`
* A self-test section (`if __name__ == "__main__": ...`)

---

## 📂 Suggested Project Layout

```
car_tools/
│
├── can_tools/
│   ├── auto_generate_can_msg.py      ← DBC → Python code generator
│   ├── generate_0xID.py             ← Generated CAN FD message module
│   └── README.md                     ← (this file)
```

---

## 🧠 Notes

* Works for both **big-endian (Motorola)** and **little-endian (Intel)** signals.
* Supports **CAN FD (up to 64 bytes)** frame generation.
* The debug flag provides detailed byte-level tracing — useful for validation or hardware testing.

---

## 🧾 License

MIT License © 2025 [LarryMai](https://github.com/LarryMai)

---

> **Next step:**
> Upload this file to
> 👉 [`car_tools/can_tools/README.md`](https://github.com/LarryMai/car_tools/tree/main/can_tools)
