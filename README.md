# Simon_Desktop_Assistant (Autonomous Windows Task Executor)

This is a Python-based autonomous AI assistant designed to **interpret human language and control your Windows PC** using the mouse, keyboard, and AI-generated instructions. It can open and control applications, type, click, read screen text (OCR), and even generate full programming projects.

---

## 🚀 Features

- **Natural language command execution**  
- **Multi-step task planning and execution**  
- **Mouse/keyboard automation (via pyautogui)**  
- **Window detection and control (via pywinauto)**  
- **Screen reading with OCR (Tesseract + OpenCV)**  
- **File-aware context memory**  
- **Code generation (Mixtral/Mistral model)**  
- **Personal memory + task history recall**

---

## 🛠️ Setup Instructions

1. Clone the repo:
 
2. Create and activate a virtual environment (optional but recommended):


3. Install dependencies:
   pyautogui==0.9.54
pygetwindow==0.0.9
pywinauto==0.6.9
opencv-python==4.11.0.86
pillow==10.3.0
pytesseract==0.3.10
psutil==5.9.8


## 🧱 Project Structure

ai_assistant/ ├── main.py # Core entrypoint ├── actions.py # Defines mouse, keyboard, app behavior ├── ui.py # GUI confirm and tray icon ├── listeners.py # ESC and override listeners ├── ai_interface.py # AI model prompt integration ├── codegen_agent.py # Code and project generator ├── task_planner.py # Multi-step breakdown logic ├── window_control.py # App/window detection ├── memory.py # Remembers past tasks ├── utils.py # Logging, OCR, etc └── assets/ # Button images for screen detection

## 🧠 Example Commands

You can type natural language instructions like:

open google earth and search for New Orleans move mouse type "reminder: finish project" open notepad generate a flask app with login page read screen

yaml
Copy
Edit

---

## 🔐 Privacy & Safety

This app is **run locally only**. No keystrokes or data leave your machine unless you configure external AI APIs.

---

## 🙌 Credits

- Built with Python 3.12  
- AI model via Mistral/Mixtral or local LM Studio  
- Uses Tesseract, OpenCV, pyautogui, pywinauto

---

## 📜 License

MIT License – free to use, modify, and distribute.
