import pyautogui
import time

print("Mouse test starting in 3 seconds...")
time.sleep(3)

print("Moving to top-left corner")
pyautogui.moveTo(100, 100, duration=1)

print("Now moving to center of screen")
screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(screenWidth / 2, screenHeight / 2, duration=1)

print("Clicking center...")
pyautogui.click()

print("Mouse test complete.")
