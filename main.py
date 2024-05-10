from vars.config import API_KEY_AV, API_KEY_P, API_KEY_FMP
from api.daily import return_daily_trades
from api.news import return_news
from api.metrics import return_metrics
from vars.file_location import current_csv, past_csv
from test_.backtest import test_past, test_current
from utils.helpers import (
    combine_cur_stocks_news,
    combine_past_stocks_news,
    return_df,
    save_to_csv,
)
import pandas as pd
import numpy as np
import os
from datetime import datetime


def current(SYMBOL, TOPIC):
    """Processes for current Stocks with recent news sentiment"""
    today = datetime.now()
    year, month, day, hour, minute = (
        today.year,
        today.month,
        today.day,
        today.hour,
        today.minute,
    )
    time_frame = test_current(year, month, day, hour, minute)
    print(f"Currently processing {TOPIC}..............")
    news = return_news(
        SYMBOL,
        TOPIC,
        API_KEY_AV,
        time_frame["news_START_DATE"],
        time_frame["news_END_DATE"],
    )
    df = return_df(time_frame)
    print("------------------------------------")
    for top_stock in news["Ticker"].values:
        print(f"Currently processing {top_stock}...........")
        if top_stock.isalpha():
            metrics = return_metrics(API_KEY_FMP, top_stock)
            try:
                daily = return_daily_trades(
                    top_stock,
                    API_KEY_P,
                    time_frame["stock_END_DATE"],
                    time_frame["current_DATE"],
                )
            except:
                print(f"daily not available for {top_stock}")
                continue
            df = pd.concat(
                [
                    df if not df.empty else None,
                    combine_cur_stocks_news(
                        top_stock,
                        daily,
                        metrics,
                        news[news.Ticker == top_stock]["Score"].values[0],
                    ),
                ],
                ignore_index=True,
            )
    return df.copy()


def past(SYMBOL, TOPIC, year, month, day, hour, minute):
    """Processes for past stocks with past news sentiment"""
    time_frame = test_past(year, month, day, hour, minute)
    if TOPIC:
        print(f"Currently processing {TOPIC}..............")
    news = return_news(
        SYMBOL,
        TOPIC,
        API_KEY_AV,
        time_frame["news_START_DATE"],
        time_frame["news_END_DATE"],
    )
    df = return_df(time_frame)
    for top_stock in news["Ticker"].values:
        if (top_stock.isalpha()) and (top_stock not in seen):
            print(f"Currently processing {top_stock}...........")
            try:
                metrics = return_metrics(API_KEY_FMP, top_stock)
                current = return_daily_trades(
                    top_stock,
                    API_KEY_P,
                    time_frame["stock_END_DATE"],
                    time_frame["current_DATE"],
                )
                past = return_daily_trades(
                    top_stock,
                    API_KEY_P,
                    time_frame["stock_START_DATE"],
                    time_frame["stock_END_DATE"],
                )
                df = pd.concat(
                    [
                        df if not df.empty else None,
                        combine_past_stocks_news(
                            top_stock,
                            past,
                            current,
                            metrics,
                            news[news.Ticker == top_stock]["Score"].values[0],
                        ),
                    ],
                    ignore_index=True,
                )
                seen.add(top_stock)
            except:
                print(f"daily not available for {top_stock}")
                continue
    return df.copy()


if __name__ == "__main__":
    TOPICS = [
        "technology",
        "finance",
        "life_sciences",
        # "economy_monetary",
        # "economy_macro",
        # "energy_transportation",
        # "mergers_and_acquisitions",
        # "retail_wholesale",
        # "real_estate",
    ]
    SYMBOLS = []
    seen = set(pd.read_csv("data/stocks_past.csv")["Ticker"].values)
    if SYMBOLS:
        for symbol in SYMBOLS:
            if symbol not in seen:
                try:
                    print(f"Analyzing stocks related to {symbol}")
                    df = past(symbol, "", 2022, 6, 15, 12, 0)
                    save_to_csv(df)
                except:
                    save_to_csv(df)
    else:
        for topic in TOPICS:
            df = past("", topic, 2022, 10, 15, 12, 0)
            save_to_csv(df)
