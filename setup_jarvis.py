import os

folders = [
    "jarvis-project",
    "jarvis-project/assets",
    "jarvis-project/.streamlit"
]

files = [
    "jarvis-project/jarvis.py",
    "jarvis-project/jarvis_brain.py",
    "jarvis-project/config.py",
    "jarvis-project/requirements.txt",
    "jarvis-project/.env",
    "jarvis-project/assets/jarvis_logo.png",
    "jarvis-project/assets/ai-thinking.json",
    "jarvis-project/.streamlit/config.toml"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w") as f:
        f.write("")

print("✅ Jarvis project structure created successfully.")
