import requests 
import json
import pandas as pd
import copy


def return_news(SYMBOLS, API_KEY):
    ### Retrieve data using API
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={SYMBOLS}&apikey={API_KEY}&sort=RELEVANCE'
    r = requests.get(url)
    data = r.json()
    return data


