import os
import streamlit as st
import pandas as pd

from api_client import fetch_news
from sentiment import analyze_sentiment
import visualizer as vz

# 🔥 clustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(page_title="뉴스 감정 분석", layout="wide")

st.title("☕ 스타벅스 뉴스 분석 대시보드")

query = st.text_input("검색 키워드", "starbucks")

if st.button("분석 시작"):

    # =========================
    # 1. 데이터 수집
    # =========================
    data = fetch_news(query, total=100)

    st.write("RAW 기사 수:", len(data))

    df = pd.DataFrame(data)

    if df.empty:
        st.error("데이터 없음")
        st.stop()

    # =========================
    # 2. 전처리
    # =========================
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    df["text"] = (df["title"] + " " + df["description"]).str.strip()

    # 🔥 date 필수 생성 (시간 그래프용)
    df["date"] = pd.to_datetime(df["publishedAt"], errors="coerce")

    # =========================
    # 3. 클러스터링
    # =========================
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(df["text"])

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    # =========================
    # 4. 감정 분석
    # =========================
    results = df["text"].apply(analyze_sentiment)
    df["sentiment"] = results.apply(lambda x: x[0])
    df["score"] = results.apply(lambda x: x[1])

    # =========================
    # 5. 디버그
    # =========================
    st.write("최종 데이터 수:", len(df))
    st.dataframe(df[["title", "cluster", "sentiment"]].head())

    st.success("분석 완료!")

    # =========================
    # 6. 시각화
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(vz.sentiment_pie(df), use_container_width=True)

    with col2:
        st.plotly_chart(vz.sentiment_bar(df), use_container_width=True)

    st.subheader("📈 시간별 감정 변화")
    st.plotly_chart(vz.sentiment_timeline(df), use_container_width=True)

    st.subheader("🧠 클러스터별 감정 분석")
    st.plotly_chart(vz.cluster_sentiment_bar(df), use_container_width=True)
