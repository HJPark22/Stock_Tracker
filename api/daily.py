import requests
import json
import pandas as pd
import copy
import time
import numpy as np


def return_data(SYMBOL, API_KEY, START_DATE, END_DATE):
    """Retrieve data using API"""
    url = f"https://api.polygon.io/v2/aggs/ticker/{SYMBOL}/range/1/day/{START_DATE}/{END_DATE}?adjusted=true&sort=asc&limit=300&apiKey={API_KEY}"
    request = requests.get(url)
    data = request.json()
    return data


def aggregate_stats(df):
    """Use to aggregate statistics"""
    open_diff = (df.loc[len(df) - 1, "Open"] - df.loc[0, "Open"]) / df.loc[0, "Open"]
    avg_vol = df["Volume"].mean()
    latest_price = df.loc[len(df) - 1, "Open"]
    initial_price = df.loc[0, "Open"]
    return (initial_price, latest_price, open_diff, avg_vol)


def preprocess_daily_data(read_in):
    """Use the Read in File to return dataframe"""
    stock_data = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    t = read_in["results"]
    for date in t:

        temp = pd.DataFrame(
            {
                "Open": [date["o"]],
                "High": [date["h"]],
                "Low": [date["l"]],
                "Close": [date["c"]],
                "Volume": [date["v"]],
            }
        )
        stock_data = pd.concat(
            [stock_data if not stock_data.empty else None, temp], ignore_index=True
        )
    return copy.deepcopy(stock_data)


def return_daily_trades(SYMBOL, API_KEY, START_DATE, END_DATE):
    data = return_data(SYMBOL, API_KEY, START_DATE, END_DATE)
    output = preprocess_daily_data(data)
    time.sleep(15)
    return output


# def return_past(df, SYMBOL):
#    '''Return historical statistics of data'''
#    hist_price, hist_change, avg_volume = aggregate_past(df)
