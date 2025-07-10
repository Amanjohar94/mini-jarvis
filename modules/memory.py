# modules/memory.py

import json
import os

MEMORY_FILE = "data/memory.json"

# Load memory from file
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

# Save memory to file
def save_memory(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

