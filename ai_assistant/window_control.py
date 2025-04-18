# window_control.py
from pywinauto import Application
from ai_assistant.utils import log_action


def list_open_windows():
    try:
        app = Application(backend="uia")
        windows = app.windows()
        for w in windows:
            log_action(f"[🪟] Window: {w.window_text()}")
    except Exception as e:
        log_action(f"[!] Error listing windows: {e}")


def activate_window_by_title(title):
    try:
        app = Application(backend="uia").connect(title_re=title)
        win = app.window(title_re=title)
        win.set_focus()
        win.maximize()
        log_action(f"[✅] Activated and maximized: {title}")
    except Exception as e:
        log_action(f"[!] Could not activate window '{title}': {e}")


def close_window_by_title(title):
    try:
        app = Application(backend="uia").connect(title_re=title)
        win = app.window(title_re=title)
        win.close()
        log_action(f"[❌] Closed window: {title}")
    except Exception as e:
        log_action(f"[!] Could not close window '{title}': {e}")
