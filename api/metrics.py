import requests
import pandas as pd
from collections import defaultdict
import copy
import numpy as np


def preprocess_metrics(data):
    d = defaultdict(list)
    for year in data:
        d["roe"].append(year["roe"])
        d["roic"].append(year["roic"])
        d["earningsYield"].append(year["earningsYield"])
        d["freeCashFlowYield"].append(year["freeCashFlowYield"])
        d["debtToEquity"].append(year["debtToEquity"])
    for item in d:
        d[item] = list(reversed(d[item]))
    return copy.deepcopy(d)


def return_metrics(API_KEY_FMP, SYMBOL):
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{SYMBOL}?period=annual&apikey={API_KEY_FMP}"
    r = requests.get(url)
    data = r.json()
    processed_data = preprocess_metrics(data)
    output = defaultdict(list)
    for item in processed_data:
        output[item + "_avg"] = find_avg(processed_data[item])
        output[item + "_trend"] = find_trend(processed_data[item])
    return copy.deepcopy(output)


# Function to find the trend of moving average
def find_trend(data):
    return np.mean(np.gradient(data))


def find_avg(data):
    return np.mean(data)
