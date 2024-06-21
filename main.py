import openai
from PIL import ImageGrab, Image
import keyboard
import base64
import os
import requests
import time
import simpleaudio

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
            {"type": "text", "text": "Answer the question shown on the screen with up to two sentences"},
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

def create_audio_file(input_text,path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "tts-1",
        "voice": "alloy",
        "input": input_text,
        "response_format": "wav"
    }

    response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=payload)
    if response.status_code == 200:
        with open(path, "wb") as audio_file:
            audio_file.write(response.content)
    else:
        print(f"Failed to generate speech: {response.status_code} - {response.text}")

def play_audio(path):
    wave_obj = simpleaudio.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


path = "screenshots/screenshot.png"
audio_path = "audio/audio.wav"

count = 0
while True:
    if keyboard.is_pressed("F7"):# and count == 0:
        count = 1
        take_screenshot(path)
        response = extract_text(path)
        response_text = response["choices"][0]["message"]["content"]
        print(response_text)
        create_audio_file(response_text,audio_path)
        play_audio(audio_path)
        print("played audio")

 
    time.sleep(0.1)
    count = 0

