import requests
import os
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def fetch_news(query="starbucks", lang="en", total=100):

    url = "https://gnews.io/api/v4/search"

    all_articles = []

    pages = total // 10

    for i in range(pages):

        params = {
            "q": query,
            "lang": lang,
            "max": 10,
            "token": GNEWS_API_KEY,
            "page": i + 1
        }

        res = requests.get(url, params=params)

        if res.status_code != 200:
            continue

        data = res.json()
        all_articles.extend(data.get("articles", []))

    return all_articles