from vars.config import API_KEY_AV, API_KEY_P
from api.daily import return_daily_trades, aggregate_stats
from api.news import symbols_to_api
from api.news import return_news
from vars.stocks import one_day_earlier, one_year_earlier
from test_.backtest import (
    news_START_DATE,
    news_END_DATE,
    stock_START_DATE,
    stock_END_DATE,
    current_DATE,
)
import requests
import pandas as pd
import numpy as np


def combine_stocks_news(SYMBOL, past, current, score):
    """Combine past and current to create df"""
    cur = pd.DataFrame(
        [
            {
                "Ticker": SYMBOL,
                "Score": score,
                "initial_price": past[0],
                "hist_change": past[2],
                "hist_price": past[1],
                "current_change": current[2],
                "current_price": current[1],
                "avg_vol": np.mean([past[3], current[3]]),
            }
        ]
    )
    return cur


if __name__ == "__main__":
    SYMBOL = "TSLA"
    temp = return_news(SYMBOL, API_KEY_AV, news_START_DATE, news_END_DATE)
    df = pd.DataFrame(
        columns=[
            "Ticker",
            "Score",
            "initial_price",
            "hist_change",
            "hist_price",
            "current_change",
            "current_price",
            "avg_vol",
        ]
    )
    for top_stock in temp["Ticker"].values:
        if top_stock.isalpha():
            past = aggregate_stats(
                return_daily_trades(
                    top_stock, API_KEY_P, stock_START_DATE, stock_END_DATE
                )
            )
            current = aggregate_stats(
                return_daily_trades(top_stock, API_KEY_P, stock_END_DATE, current_DATE)
            )
            df = pd.concat(
                [
                    df if not df.empty else None,
                    combine_stocks_news(
                        top_stock,
                        past,
                        current,
                        temp[temp.Ticker == top_stock]["Score"],
                    ),
                ],
                ignore_index=True,
            )
    print(df)
print(6)
