import requests
import json
import pandas as pd
import copy

'''"sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish;
 -0.15 < x < 0.15: Neutral; 0.15 <= x < 0.35: Somewhat_Bullish; x >= 0.35: Bullish"'''

SYMBOLS = ["TSLA", "AAPL"]


# Need to fix this error
def symbols_to_api(SYMBOLS):
    api_string = ",".join(SYMBOLS)
    return api_string


### Helper for preprocess_data
def aggregate_news_data(df):
    """helper to preprocess data"""

    most_label = df.groupby("Ticker")["Label"].agg(pd.Series.mode).reset_index()
    mean_score = df.groupby("Ticker")["Score"].mean().reset_index()
    counter = df.groupby("Ticker")["Label"].count().reset_index(name="Count")
    result_df = most_label.merge(mean_score, on="Ticker")
    result_df = result_df.merge(counter, on="Ticker")

    return copy.deepcopy(result_df)


def above_threshold(df, threshold, no_mention):
    """helper to return stocks mentioned frequently above threshold"""

    output = df[(df.Score > threshold) & (df.Count > no_mention)][["Ticker", "Score"]]

    return output


def preprocess_news_data(read_in):
    """Preprocess news data"""

    news_data = pd.DataFrame(columns=["Ticker", "Score", "Label"])

    articles = read_in["feed"]

    for article in articles:
        ticker = article["ticker_sentiment"]
        for tick in ticker:
            if tick["relevance_score"] > "0.2":
                temp = pd.DataFrame(
                    [
                        {
                            "Ticker": tick["ticker"],
                            "Score": tick["ticker_sentiment_score"],
                            "Label": tick["ticker_sentiment_label"],
                        }
                    ]
                )
                news_data = pd.concat([news_data, temp], ignore_index=True)

    news_data["Score"] = pd.to_numeric(news_data["Score"], errors="coerce")
    final_news_data = aggregate_news_data(news_data)
    top_stocks = above_threshold(final_news_data, 1.0, 5)

    return copy.deepcopy(top_stocks)


def return_news(SYMBOLS, API_KEY, TIME_FROM, TIME_TO):
    """Retrieve data using API"""

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={SYMBOLS}&apikey={API_KEY}&sort=RELEVANCE&limit=1000&time_from={TIME_FROM}&time_to={TIME_TO}"
    r = requests.get(url)
    data = r.json()
    output = preprocess_news_data(data)

    return output
