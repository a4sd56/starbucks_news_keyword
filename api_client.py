import requests
import streamlit as st

GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"]


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
            "sortby": "publishedAt"
        }

        res = requests.get(url, params=params, timeout=10)

        # 🔥 중요: 실패 숨기지 않음
        if res.status_code != 200:
            st.error(f"API Error: {res.status_code}")
            st.write(res.text)
            continue

        data = res.json()
        articles = data.get("articles", [])

        all_articles.extend(articles)

    return all_articles
