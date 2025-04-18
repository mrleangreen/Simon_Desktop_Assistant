# utils.py
import time
import threading
import pyautogui
import tkinter as tk
import pytesseract
from PIL import Image
from .state import get_manual_override, set_manual_override

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

action_log = []

def log_action(action):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}"
    action_log.append(entry)
    print(entry)
    with open("action_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(entry + "\n")

def check_resume():
    if get_manual_override():
        log_action("[!] Task paused due to manual override.")
        resume = input("Resume AI task? (y/n): ").strip().lower()
        if resume == "y":
            set_manual_override(False)
            log_action("[✔] Resuming...")
            return True
        else:
            log_action("[x] Task permanently canceled.")
            return False
    return True

def ripple_cursor():
    def run_ripple():
        global ripple_window
        ripple_window = tk.Tk()
        ripple_window.overrideredirect(True)
        ripple_window.attributes("-topmost", True)
        ripple_window.attributes("-transparentcolor", "white")
        ripple_window.config(bg="white")

        canvas = tk.Canvas(ripple_window, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack()

        def update():
            if not ripple_cursor.running:
                ripple_window.destroy()
                return
            x, y = pyautogui.position()
            ripple_window.geometry(f"+{x - 50}+{y - 50}")
            canvas.delete("all")
            canvas.create_oval(20, 20, 80, 80, outline="#00ffff", width=2)
            canvas.create_oval(30, 30, 70, 70, outline="#00ffff", width=1)
            ripple_window.after(100, update)

        ripple_cursor.running = True
        update()
        ripple_window.mainloop()

    threading.Thread(target=run_ripple, daemon=True).start()

def stop_ripple():
    ripple_cursor.running = False

def read_screen_text():
    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)
    log_action("[📷] Screen OCR captured:")
    log_action(text.strip())
    show_text_popup(text.strip())
    return text

def show_text_popup(text):
    popup = tk.Tk()
    popup.title("OCR Result")
    popup.geometry("600x400")
    text_box = tk.Text(popup, wrap="word", font=("Segoe UI", 11))
    text_box.insert("1.0", text)
    text_box.pack(expand=True, fill="both")
    popup.mainloop()
