import requests
import streamlit as st
import time

GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"]


@st.cache_data(ttl=3600)
def fetch_news(query="starbucks", lang="en", total=100):

    url = "https://gnews.io/api/v4/search"

    # 🔥 query 확장 (중복 줄이고 다양성 확보)
    queries = [
        query,
        f"{query} korea",
        f"{query} controversy",
        f"{query} boycott",
        f"{query} news"
    ]

    all_articles = []

    for q in queries:

        time.sleep(1)  # 🔥 rate limit 방지

        params = {
            "q": q,
            "lang": lang,
            "max": 10,
            "token": GNEWS_API_KEY,
            "sortby": "publishedAt"
        }

        res = requests.get(url, params=params, timeout=10)

        if res.status_code != 200:
            st.error(f"API Error: {res.status_code}")
            st.write(res.text)
            continue

        data = res.json()
        all_articles.extend(data.get("articles", []))

    # 🔥 중복 제거
    seen = set()
    unique = []

    for a in all_articles:
        key = a.get("title", "")
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique[:total]
