# listeners.py
from pynput import keyboard, mouse
import threading
from ai_assistant.state import set_cancel_task, set_manual_override


def listen_escape():
    def on_press(key):
        if key == keyboard.Key.esc:
            print("[!] ESC pressed – canceling task.")
            set_cancel_task(True)
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def listen_right_click():
    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.right:
            print("[!] Right-click – manual override triggered.")
            set_manual_override(True)
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def start_listeners():
    esc_thread = threading.Thread(target=listen_escape)
    click_thread = threading.Thread(target=listen_right_click)
    esc_thread.start()
    click_thread.start()
    return esc_thread, click_thread

