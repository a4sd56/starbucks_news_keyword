import requests
import streamlit as st
import time

GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"]


# 🔥 캐싱은 여기 붙임 (핵심)
@st.cache_data(ttl=3600)
def fetch_news(query="starbucks", lang="en", total=50):

    url = "https://gnews.io/api/v4/search"

    all_articles = []

    pages = total // 10

    for i in range(pages):

        time.sleep(1)  # 🔥 rate limit 방지

        params = {
            "q": query,
            "lang": lang,
            "max": 10,
            "token": GNEWS_API_KEY,
            "sortby": "publishedAt"
        }

        res = requests.get(url, params=params, timeout=10)

        # 실패 출력
        if res.status_code != 200:
            st.error(f"API Error: {res.status_code}")
            st.write(res.text)
            continue

        data = res.json()
        all_articles.extend(data.get("articles", []))

    return all_articles
