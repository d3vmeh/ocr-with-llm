import openai
from PIL import ImageGrab, Image
import keyboard
import base64
import os
import requests
import time

api_key = os.getenv("OPENAI_API_KEY")


def take_screenshot(path):
    screenshot = ImageGrab.grab()
    screenshot.save(path)

def encode_image(path):
    image = open(path, "rb")
    return base64.b64encode(image.read()).decode('utf8')

def extract_text(path):
    encoded_image = encode_image(path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Answer the question shown on the screen"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{encoded_image}", "detail": "low"}}
        ]
    }

    payload = {
        "model": "gpt-4o",
        "temperature": 0.5,
        "messages": [message],
        "max_tokens": 800
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()


path = "screenshots/screenshot.png"
count = 0
while True:

    if keyboard.is_pressed("F3") and count == 0:
        count = 1
        take_screenshot(path)
        response = extract_text(path)
        print(response["choices"][0]["message"]["content"])

    time.sleep(0.2)
    count = 0

