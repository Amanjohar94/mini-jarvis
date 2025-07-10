# modules/weather.py

import requests

def get_weather(city="Delhi"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return "🌤️ " + response.text.strip()
        return f"⚠️ Failed to fetch weather for {city}"
    except Exception as e:
        return f"❌ Error: {e}"

