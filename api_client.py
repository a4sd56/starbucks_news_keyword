import requests
import streamlit as st
import time

GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"]


# 🔥 여러 키워드로 확장해서 진짜 100개 확보
def fetch_news(query="starbucks", lang="en", total=100):

    url = "https://gnews.io/api/v4/search"

    # 🔥 핵심: query 확장 (중복 방지 핵심)
    queries = [
        query,
        f"{query} korea",
        f"{query} controversy",
        f"{query} boycott",
        f"{query} news"
    ]

    all_articles = []

    per_query = max(10, total // len(queries))

    for q in queries:
        
        time.sleep(1)
        
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
        articles = data.get("articles", [])

        all_articles.extend(articles)

    # 🔥 중복 제거 (핵심)
    seen = set()
    unique_articles = []

    for a in all_articles:
        key = a.get("title", "")

        if key not in seen:
            seen.add(key)
            unique_articles.append(a)

    return unique_articles[:total]
