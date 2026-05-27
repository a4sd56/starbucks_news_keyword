import os
import streamlit as st
import pandas as pd

from api_client import fetch_news
from sentiment import analyze_sentiment
import visualizer as vz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.title("☕ 뉴스 감정 + 클러스터링 대시보드")

query = st.text_input("검색어", "starbucks")

if st.button("분석 시작"):

    # 1. 데이터 수집 (100개)
    data = fetch_news(query, total=100)

    df = pd.DataFrame(data)

    if df.empty:
        st.error("데이터 없음")
        st.stop()

    # 2. 날짜 처리
    df["date"] = df["publishedAt"]

    # 3. text 생성
    df["text"] = (
        df["title"].fillna("") + " " + df["description"].fillna("")
    )

    # 4. 🔥 중복 제거 (핵심)
    df = df.drop_duplicates(subset="title")

    # 5. 감정 분석
    results = df["text"].apply(analyze_sentiment)
    df["sentiment"] = results.apply(lambda x: x[0])
    df["score"] = results.apply(lambda x: x[1])

    # 6. 🔥 클러스터링 (핵심)
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["text"])

    k = 5  # 클러스터 개수
    model = KMeans(n_clusters=k, random_state=42, n_init=10)

    df["cluster"] = model.fit_predict(X)

    st.success("분석 완료!")

    # 7. 데이터 확인
    st.subheader("데이터")
    st.dataframe(df)

    # 8. 시각화
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(vz.sentiment_pie(df), use_container_width=True)

    with col2:
        st.plotly_chart(vz.sentiment_bar(df), use_container_width=True)

    st.subheader("시간별 감정")
    st.plotly_chart(vz.sentiment_timeline(df), use_container_width=True)

    # 9. 🔥 클러스터 결과
    st.subheader("🧠 클러스터 분석")

    for i in range(k):
        st.markdown(f"### Cluster {i}")
        st.write(df[df["cluster"] == i][["title"]].head(5))