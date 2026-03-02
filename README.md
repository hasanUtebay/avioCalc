# AvioCalc - Aviation Flight Computer

AvioCalc is a Python-based desktop application designed to assist pilots and flight simulator enthusiasts with critical in-flight calculations. Developed with a modern GUI, it simplifies descent planning and holding pattern entry analysis.

## 🚀 Features

### 📉 Descent Computer

Calculate your descent profile accurately to ensure you reach your target altitude at the right time and distance.

Required Net VS: Calculates the exact Vertical Speed (fpm) needed.

Set VS: Suggests a rounded Vertical Speed for easier autopilot input.

Start Descent Point: Calculates the exact distance (NM) where you should begin your descent.

![Descent Computer](/descent_computer.png "Descent Computer")

### 🔄 Holding Computer

Analyze the best way to enter a holding pattern based on your current heading and the holding course.

Entry Types: Identifies Direct, Parallel, or Teardrop entries.

Standard & Non-Standard: Supports both Right-hand (Standard) and Left-hand (Non-Standard) turns.

Step-by-Step Instructions: Provides clear, textual instructions for both the entry phase and the holding phase.

![Holding Computer](/holding_computer.png "Holding Computer")

### 🛠️ Installation

Prerequisites

- Python 3.x

- Pillow (PIL) library for image processing.

- Tkinter (usually comes with Python).

### Setup

Clone the repository:

```
Bash
git clone https://github.com/yourusername/aviocalc.git
Install the required dependency:
```

```
Bash
pip install Pillow
Run the application:
```

```
Bash
python main.py
```

### 🖥️ User Interface

The application features a dark-themed, user-friendly interface:

Modern Aesthetics: Dark mode design with high-contrast accent colors for readability.

Smart Input Validation: Supports various number formats (commas/periods) and prevents invalid data entry.

Responsive Feedback: Real-time warnings if altitude logic is incorrect (e.g., target higher than current).

### 👨‍💻 Developer

Created by Hasan ÜTEBAY.

This tool is designed for flight simulation and educational purposes. Always cross-check with official aeronautical charts and instruments during real-world flight operations.

### 📄 License

This project is open-source and available under the MIT License.
