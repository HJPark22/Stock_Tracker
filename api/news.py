import requests 
import json
import pandas as pd
import copy

'''"sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish;
 -0.15 < x < 0.15: Neutral; 0.15 <= x < 0.35: Somewhat_Bullish; x >= 0.35: Bullish"'''

SYMBOLS = ["TSLA", "AAPL"]


# Need to fix this error
def symbols_to_api(SYMBOLS):
    api_string = ','.join(SYMBOLS)
    return api_string

### Helper for preprocess_data
def helper1(df):
    '''helper to preprocess data'''

    most_label = df.groupby('Ticker')['Label'].agg(pd.Series.mode).reset_index()
    mean_score = df.groupby('Ticker')['Score'].mean().reset_index()
    result_df = most_label.merge(mean_score, on='Ticker')

    return copy.deepcopy(result_df)


def preprocess_news_data(read_in):
    '''Preprocess news data'''

    news_data = pd.DataFrame(columns=['Ticker','Score','Label'])
   
    articles = read_in['feed']

    for article in articles:
        ticker = article['ticker_sentiment']
        for tick in ticker:
            temp = pd.DataFrame([{'Ticker': tick['ticker'], "Score": tick['ticker_sentiment_score'],\
                                        "Label": tick['ticker_sentiment_label']}])
            news_data = pd.concat([news_data, temp], ignore_index=True)
    
    news_data['Score'] = pd.to_numeric(news_data['Score'], errors='coerce')
    final_news_data = helper1(news_data)

    return copy.deepcopy(final_news_data)



def return_news(SYMBOLS, API_KEY):
    '''Retrieve data using API'''
    
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={SYMBOLS}&apikey={API_KEY}&sort=RELEVANCE&limit=1000'
    r = requests.get(url)
    data = r.json()
    output = preprocess_news_data(data)
    
    return output


