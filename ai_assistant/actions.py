import subprocess
import time
import os
import cv2
import pyautogui
import pygetwindow as gw
from pyautogui._pyautogui_win import _moveTo as moveTo
from ai_assistant.utils import log_action, check_resume, read_screen_text, ripple_cursor, stop_ripple
from ai_assistant.state import cancel_task, manual_override
from PIL import Image

def run_action(action):
    global cancel_task, manual_override
    cancel_task = False
    manual_override = False

    start_time = time.time()
    log_action(f"[🤖] Executing: {action}")

    if not check_resume():
        return

    action = action.lower()

    if action.startswith("input "):
        action = "type " + action[6:]
    elif action.startswith("search "):
        action = "type " + action[7:]

    steps = [step.strip() for step in action.split("&&") if step.strip()]
    location = ""
    for step in steps:
        if step.startswith("search ") or step.startswith("type "):
            location = step.split(" ", 1)[-1].strip().strip('"')

    for step in steps:
        if not check_resume():
            break

        if (
            "open google earth" in step or
            ("google" in step and "earth" in step and ("open" in step or "start" in step or ".exe" in step))
        ):
            subprocess.Popen(r"C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe")
            for i in range(15):
                time.sleep(1)
                if not check_resume():
                    return

            try:
                window = gw.getWindowsWithTitle("Google Earth")[0]
                window.activate()
                window.maximize()
                log_action("[🪟] Activated and maximized Google Earth window.")
                time.sleep(1)
            except Exception as e:
                log_action(f"[!] Could not activate window: {e}")

            action_clean = step.replace("\n", " ").replace("  ", " ")

            if not location:
                if "type" in action_clean:
                    location = action_clean.split("type", 1)[-1].strip().strip('"')
                elif "search for" in action_clean:
                    location = action_clean.split("search for", 1)[-1].strip().strip('"')

            log_action(f"[🔍] Parsed location: '{location}'")

            try:
                ripple_cursor()
            except Exception as e:
                log_action(f"[!] Ripple error: {e}")

            full_path = os.path.abspath("assets/google_earth_search.png")
            new_path = os.path.abspath("assets/verified_google_earth_search.png")
            log_action(f"[🧪] Full image path: {full_path}")

            try:
                img = Image.open(full_path).convert("RGB")
                img.save(new_path, format="PNG")
                log_action(f"[✔] Image re-saved as: {new_path}")
                log_action("[✔] Image re-saved as clean PNG.")
            except Exception as e:
                log_action(f"[!] Failed to re-save image: {e}")

            test_img = cv2.imread(full_path)
            if test_img is None:
                log_action("[❌] OpenCV failed to read the image file.")
            else:
                log_action("[✅] OpenCV successfully loaded the search icon.")

            try:
                search_icon = pyautogui.locateCenterOnScreen(new_path, confidence=0.7)
                if search_icon:
                    log_action(f"[🖱️] Found search bar at {search_icon}, clicking...")
                    pyautogui.moveTo(search_icon[0], search_icon[1], duration=1.2)
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.write(location, interval=0.05)
                    pyautogui.press("enter")
                    log_action(f"[🌍] Google Earth searched for: {location}")
                else:
                    log_action("[❌] Could not find search bar on screen. Screenshot saved.")
                    pyautogui.screenshot("search_debug.png")
            except Exception as e:
                log_action(f"[!] Error locating image on screen: {e}")

            stop_ripple()

        elif "open chrome" in step:
            subprocess.Popen("chrome")
            time.sleep(2)
            ripple_cursor()
            pyautogui.write("New Orleans Louisiana", interval=0.05)
            pyautogui.press("enter")
            stop_ripple()

        elif "open notepad" in step:
            subprocess.Popen("notepad.exe")
            time.sleep(1)
            if not check_resume():
                return
            ripple_cursor()
            pyautogui.write(
                "Todo List:\n- Complete project report\n- Call John\n- Grocery shopping\n- Submit expense report\n- Book travel for next meeting",
                interval=0.05
            )
            stop_ripple()

        elif "move mouse" in step:
            ripple_cursor()
            for _ in range(5):
                if cancel_task:
                    stop_ripple()
                    log_action("[x] Task canceled.")
                    return
                if not check_resume():
                    stop_ripple()
                    return
                moveTo(200, 200, duration=1)
                moveTo(800, 400, duration=1)
            stop_ripple()

        elif "type " in step:
            text = step.split("type", 1)[-1].strip().strip('"')
            if not check_resume():
                return
            ripple_cursor()
            pyautogui.write(text, interval=0.05)
            pyautogui.press("enter")
            stop_ripple()

        elif "press " in step:
            key = step.split("press", 1)[-1].strip()
            ripple_cursor()
            pyautogui.press(key)
            log_action(f"[⌨️] Pressed key: {key}")
            stop_ripple()

        elif step == "click":
            ripple_cursor()
            pyautogui.click()
            log_action("[🖱️] Clicked at current mouse position.")
            stop_ripple()

        elif "read screen" in step:
            read_screen_text()

        else:
            log_action(f"[-] No recognized action to perform in: '{step}'")

    elapsed = round(time.time() - start_time, 2)
    log_action(f"[⏱] Task completed in {elapsed} seconds")




