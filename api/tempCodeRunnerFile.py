import requests 
import json


def return_daily_trades(SYMBOL, API_KEY):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    return data