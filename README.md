# 🌡️📊 Temperature Sensor Data Parser

A modern desktop application built with Python and CustomTkinter designed to parse, sanitize, normalize, and summarize unstructured hardware temperature logs and weather telemetry.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6aa5)](https://github.com/TomSchimansky/CustomTkinter)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 💡 Overview

Industrial microcontrollers, weather stations, and hardware sensors (e.g., ESP32, Arduino, Raspberry Pi) often generate raw text telemetry across mixed metric, imperial, and thermodynamic scales:
- Ingests raw `.txt` and `.log` hardware telemetry line-by-line using defensive file parsing loops.
- Employs tokenization and index slicing to isolate timestamps, sensor device IDs, raw temperature strings, and status flags.
- Dynamically strips unit qualifiers, type-casts string readings to floating-point numbers, and standardizes all values to Celsius (°C).
- Filters malformed packets, corrupted characters, and sensor `ERR` states on the fly while computing live aggregate telemetry statistics.

---

## 🛠️ Built With

- **Python 3.12** – Core programming logic, string manipulation, and mathematical parsing routines.
- **CustomTkinter** – Modern, responsive dark-mode native desktop user interface.
- **Tkinter (`filedialog`, `messagebox`)** – Native OS system file explorer dialogs and error alerts.
- **Webbrowser** – One-click external navigation for developer profiles.

---

## ⚙️ Parsing & Unit Conversion Pipeline

| Raw Unit | Input Example | Parsing Logic | Output Formula |
| :--- | :--- | :--- | :--- |
| **Celsius (`C`)** | `RAW:24.35C` | Slices numeric string, validates unit flag | $$C = C$$ |
| **Fahrenheit (`F`)** | `RAW:77.18F` | Extracts float, converts to standard metric | $$C = (F - 32) \times \frac{5}{9}$$ |
| **Kelvin (`K`)** | `RAW:298.55K` | Extracts float, shifts absolute temperature | $$C = K - 273.15$$ |
| **Corrupted / Flagged** | `RAW:INVALID` / `STATUS:ERR` | Flags anomaly, skips calculation | **DISCARDED** |

---

## 📁 Repository Structure

```text
temperature-sensor-data-parser/
│
├── main.py                  # CustomTkinter GUI application & parsing engine
├── requirements.txt         # Python package dependencies
├── README.md                # Project documentation
├── .gitignore               # Ignored files (venv, cache, local logs)
│
└── data/                    # Sample telemetry datasets
    └── sensor_logs.txt      # Raw hardware sensor output sample
```

---

## 📋 Sample Input Telemetry (`sensor_logs.txt`)

```text
2026-10-23 00:01:15 | SENSOR_ID:TMP102 | RAW:24.35C | STATUS:OK
2026-10-23 00:02:15 | SENSOR_ID:TMP102 | RAW:77.18F | STATUS:OK
2026-10-23 00:03:15 | SENSOR_ID:TMP102 | RAW:298.55K | STATUS:OK
2026-10-23 00:04:15 | SENSOR_ID:TMP102 | RAW:INVALID | STATUS:ERR
2026-10-23 00:05:15 | SENSOR_ID:TMP102 | RAW:26.10C | STATUS:OK
2026-10-23 00:06:15 | SENSOR_ID:TMP102 | RAW:81.50F | STATUS:OK
```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Rudra1725/temperature-sensor-data-parser.git](https://github.com/Rudra1725/temperature-sensor-data-parser.git)
   cd temperature-sensor-data-parser
   ```

2. **Install dependencies:**
   ```bash
   pip install customtkinter
   ```

3. **Launch the application:**
   ```bash
   python main.py
   ```

---

## 👨‍💻 Developer

**Rudra Wagh**  
- **GitHub:** [@Rudra1725](https://github.com/Rudra1725)  
- **LinkedIn:** [rudra-wagh-476a9830b](https://www.linkedin.com/in/rudra-wagh-476a9830b)

---

## 📄 License

This project is licensed under the MIT License.
