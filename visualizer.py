import plotly.express as px
import pandas as pd


def sentiment_pie(df):

    tmp = df["sentiment"].value_counts().reset_index()
    tmp.columns = ["sentiment", "count"]

    return px.pie(
        tmp,
        names="sentiment",
        values="count",
        title="감정 분포"
    )


def sentiment_bar(df):

    tmp = df["sentiment"].value_counts().reset_index()
    tmp.columns = ["sentiment", "count"]

    return px.bar(
        tmp,
        x="sentiment",
        y="count",
        title="감정 분포"
    )


def sentiment_timeline(df):

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    tmp = df.groupby(["date", "sentiment"]).size().reset_index(name="count")

    return px.line(
        tmp,
        x="date",
        y="count",
        color="sentiment",
        title="시간별 감정 변화"
    )


def cluster_sentiment_bar(df):

    tmp = df.groupby(["cluster", "sentiment"]).size().reset_index(name="count")

    return px.bar(
        tmp,
        x="cluster",
        y="count",
        color="sentiment",
        barmode="group",
        title="클러스터별 감정 분포"
    )
