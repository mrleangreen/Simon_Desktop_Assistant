# ai_interface.py
import requests

def ask_mistral(prompt):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return res.json()["response"]
