import os
import streamlit as st
import pandas as pd

from api_client import fetch_news
from sentiment import analyze_sentiment
import visualizer as vz

os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(page_title="뉴스 감정 분석", layout="wide")

st.title("☕ 스타벅스 뉴스 감정 분석")

query = st.text_input("검색 키워드", "starbucks")

if st.button("분석 시작"):

    # 🔥 뉴스 수집
    data = fetch_news(query, total=100)

    st.write("📦 수집된 raw 기사 수:", len(data))

    df = pd.DataFrame(data)

    if df.empty:
        st.error("데이터 없음")
        st.stop()

    # 🔥 결측값 처리
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    # 🔥 텍스트 생성
    df["text"] = (df["title"] + " " + df["description"]).str.strip()

    # 🔥 중복 제거 (추가 안전장치)
    df = df.drop_duplicates(subset=["title"])

    st.write("📊 중복 제거 후:", len(df))

    # 🔥 감정 분석
    results = df["text"].apply(analyze_sentiment)
    df["sentiment"] = results.apply(lambda x: x[0])
    df["score"] = results.apply(lambda x: x[1])

    st.success("분석 완료")

    st.subheader("데이터")
    st.dataframe(df)

    # 시각화
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(vz.sentiment_pie(df), use_container_width=True)

    with col2:
        st.plotly_chart(vz.sentiment_bar(df), use_container_width=True)

    st.subheader("시간별 감정 변화")
    st.plotly_chart(vz.sentiment_timeline(df), use_container_width=True)

    if "cluster" in df.columns:
        st.subheader("클러스터별 감정")
        st.plotly_chart(vz.cluster_sentiment_bar(df), use_container_width=True)
