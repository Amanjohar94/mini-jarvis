import os

NOTES_FILE = "data/notes.txt"

def save_note(note):
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(note.strip() + "\n---\n")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return f.read().split("---\n")
