import requests
from utils.config import NEWS_API_KEY

def get_top_headlines():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url)
        articles = res.json().get("articles", [])[:5]
        return [{"title": a["title"], "description": a["description"]} for a in articles]
    except Exception as e:
        return [{"title": "Error", "description": str(e)}]

