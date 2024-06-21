import openai
from PIL import ImageGrab, Image
import keyboard

def get_screenshot(path):
    screenshot = ImageGrab.grab()
    screenshot.save(path)


path = "screenshots/screenshot.png"
keyboard.add_hotkey("1", lambda: get_screenshot(path))

while True:
    keyboard.wait("esc")