import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

FEATURES = {
    "chat": True,
    "news": True,
    "weather": True,
    "tasks": True,
    "markets": True,
    # Optional:
    # "notes": True
}

VOICE_ENABLED = True  # default to unmuted

