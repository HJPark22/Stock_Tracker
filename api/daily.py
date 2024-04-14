import requests 
import json
import pandas as pd
import copy

def preprocess_data(read_in):
    ## Use the Read in File
    stock_data = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    t = read_in['Time Series (Daily)']
    for date in t:

        temp = pd.DataFrame({'Date': [date], "Open": [t[date]["1. open"]],\
                                    "High": [t[date]["2. high"]], "Low": [t[date]["3. low"]],\
                                    'Close': [t[date]["4. close"]], "Volume": [t[date]["5. volume"]]})
        stock_data = pd.concat([stock_data, temp], ignore_index=True)
    return copy.deepcopy(stock_data)



def return_daily_trades(SYMBOL, API_KEY):
    ### Retrieve data using API
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
    request = requests.get(url)
    data = request.json()
    output = preprocess_data(data)
    return output
