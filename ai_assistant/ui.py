# ui.py
import tkinter as tk
import threading
import sys
from PIL import Image, ImageDraw
import pystray


def confirm_gui(task):
    result = []

    def on_accept():
        result.append(True)
        window.destroy()

    def on_decline():
        result.append(False)
        window.destroy()

    window = tk.Tk()
    window.title("AI Task Request")
    window.geometry("450x200")
    window.configure(bg="#2b2b2b")
    window.eval('tk::PlaceWindow . center')

    label = tk.Label(window, text=f"Should I do this task?",
                     font=("Segoe UI", 14, "bold"), fg="white", bg="#2b2b2b")
    label.pack(pady=(20, 10))

    task_label = tk.Label(window, text=task, font=("Segoe UI", 12), fg="#f5f5f5",
                          bg="#2b2b2b", wraplength=400, justify="center")
    task_label.pack(pady=(0, 20))

    button_frame = tk.Frame(window, bg="#2b2b2b")
    button_frame.pack()

    yes_btn = tk.Button(button_frame, text="Allow", command=on_accept,
                        font=("Segoe UI", 11), bg="#4caf50", fg="white", width=12)
    yes_btn.grid(row=0, column=0, padx=10)

    no_btn = tk.Button(button_frame, text="Deny", command=on_decline,
                       font=("Segoe UI", 11), bg="#f44336", fg="white", width=12)
    no_btn.grid(row=0, column=1, padx=10)

    window.mainloop()
    return result[0] if result else False


def create_tray_icon():
    def quit_action(icon, item):
        icon.stop()
        sys.exit()

    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='white')
    icon = pystray.Icon("AI Assistant", image, "AI Assistant", menu=pystray.Menu(
        pystray.MenuItem("Exit", quit_action)
    ))
    threading.Thread(target=icon.run, daemon=True).start()
