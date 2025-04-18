# memory.py
import json
import os
from datetime import datetime

MEMORY_FILE = "ai_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def remember_task(prompt, actions):
    memory = load_memory()
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "actions": actions
    })
    save_memory(memory)

def search_memory(query):
    memory = load_memory()
    return [m for m in memory if query.lower() in m["prompt"].lower()]
