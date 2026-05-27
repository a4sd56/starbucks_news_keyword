import plotly.express as px
import pandas as pd


def sentiment_pie(df):

    order = ["POSITIVE", "NEGATIVE", "NEUTRAL"]

    tmp = df["sentiment"].value_counts().reindex(order).fillna(0).reset_index()
    tmp.columns = ["sentiment", "count"]

    colors = {
        "POSITIVE": "#2ecc71",
        "NEGATIVE": "#e74c3c",
        "NEUTRAL": "#95a5a6"
    }

    fig = px.pie(
        tmp,
        names="sentiment",
        values="count",
        title="감정 분포",
        color="sentiment",
        color_discrete_map=colors
    )

    fig.update_traces(textinfo="percent+label")

    return fig


def sentiment_bar(df):

    tmp = df["sentiment"].value_counts().reset_index()
    tmp.columns = ["sentiment", "count"]

    colors = {
        "POSITIVE": "#2ecc71",
        "NEGATIVE": "#e74c3c",
        "NEUTRAL": "#95a5a6"
    }

    fig = px.bar(
        tmp,
        x="sentiment",
        y="count",
        title="감정 분포 (Bar)",
        color="sentiment",
        color_discrete_map=colors
    )

    return fig


def sentiment_timeline(df):

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    tmp = df.groupby(["date", "sentiment"]).size().reset_index(name="count")

    return px.line(tmp, x="date", y="count", color="sentiment", title="시간별 감정 변화")

def cluster_sentiment_bar(df):

    # 클러스터 + 감정 집계
    tmp = df.groupby(["cluster", "sentiment"]).size().reset_index(name="count")

    # 정렬 보기 좋게
    tmp = tmp.sort_values("cluster")

    colors = {
        "POSITIVE": "#2ecc71",
        "NEGATIVE": "#e74c3c",
        "NEUTRAL": "#95a5a6"
    }

    fig = px.bar(
        tmp,
        x="cluster",
        y="count",
        color="sentiment",
        barmode="group",  # 🔥 핵심 (비교형)
        title="클러스터별 감정 분포",
        color_discrete_map=colors
    )

    return fig