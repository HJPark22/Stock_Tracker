import requests 
import json
import pandas as pd
import copy



def preprocess_daily_data(read_in):
    ## Use the Read in File
    stock_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    t = read_in['results']
    for date in t:

        temp = pd.DataFrame({"Open": [date["o"]],\
                                    "High": [date["h"]], "Low": [date["l"]],\
                                    'Close': [date["c"]], "Volume": [date["v"]]})
        stock_data = pd.concat([stock_data, temp], ignore_index=True)
    return copy.deepcopy(stock_data)



def return_daily_trades(SYMBOL, API_KEY, START_DATE, END_DATE):
    ### Retrieve data using API
    url = f"https://api.polygon.io/v2/aggs/ticker/{SYMBOL}/range/1/day/{START_DATE}/{END_DATE}?adjusted=true&sort=asc&limit=300&apiKey={API_KEY}"
    request = requests.get(url)
    data = request.json()
    output = preprocess_daily_data(data)
    return output
