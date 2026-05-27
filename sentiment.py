from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    if not text:
        return "NEUTRAL", 0.0

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "POSITIVE", score
    elif score <= -0.05:
        return "NEGATIVE", score
    else:
        return "NEUTRAL", score