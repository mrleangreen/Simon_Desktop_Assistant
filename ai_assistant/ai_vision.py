# ai_vision.py
import cv2
import numpy as np
import pyautogui
from ai_assistant.utils import log_action


def locate_on_screen_opencv(template_path, confidence=0.8):
    try:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confidence)

        if len(loc[0]) > 0:
            pt = (loc[1][0], loc[0][0])
            log_action(f"[🔍] Match found at: {pt}")
            return pt[0] + w // 2, pt[1] + h // 2
        else:
            log_action("[❌] No match found.")
            return None
    except Exception as e:
        log_action(f"[!] OpenCV error: {e}")
        return None


def click_on_image(template_path):
    point = locate_on_screen_opencv(template_path)
    if point:
        pyautogui.moveTo(point[0], point[1], duration=1)
        pyautogui.click()
        log_action(f"[🖱️] Clicked at: {point}")
    else:
        log_action("[!] Could not click, image not found.")
