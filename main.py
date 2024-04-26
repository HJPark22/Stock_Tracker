from vars.config import API_KEY_AV, API_KEY_P, API_KEY_FMP
from api.daily import return_daily_trades, aggregate_stats
from api.news import return_news
from api.metrics import return_metrics
from vars.file_location import current_csv, past_csv
from test_.backtest import test_past, test_current
from utils.helpers import combine_cur_stocks_news, combine_past_stocks_news, return_df
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


def past(SYMBOL, year, month, day, hour, minute):
    time_frame = test_past(year, month, day, hour, minute)
    news = return_news(
        SYMBOL, API_KEY_AV, time_frame["news_START_DATE"], time_frame["news_END_DATE"]
    )
    df = return_df(time_frame)
    for top_stock in news["Ticker"].values:
        if top_stock.isalpha():
            current = aggregate_stats(
                return_daily_trades(
                    top_stock,
                    API_KEY_P,
                    time_frame["stock_END_DATE"],
                    time_frame["current_DATE"],
                )
            )
            past = aggregate_stats(
                return_daily_trades(
                    top_stock,
                    API_KEY_P,
                    time_frame["stock_START_DATE"],
                    time_frame["stock_END_DATE"],
                )
            )
            df = pd.concat(
                [
                    df if not df.empty else None,
                    combine_past_stocks_news(
                        top_stock,
                        past,
                        current,
                        news[news.Ticker == top_stock]["Score"].values[0],
                    ),
                ],
                ignore_index=True,
            )
    return df.copy()


if __name__ == "__main__":
    # TOPICS = ["energy_transportation", "technology", "life_sciences"]
    # for topic in TOPICS:
    df = current("LIN", "")
    # df = past("META", 2023, 6, 15, 12, 0)
    df.sort_values(by="Score", ascending=False, inplace=True)
    if not df.empty:
        if "initial_price" in df.columns.values:
            save_file = past_csv
        else:
            save_file = current_csv
        if os.path.getsize(save_file) == 0:
            df.to_csv(save_file, index=False)
        else:
            df.to_csv(save_file, mode="a", index=False, header=False)
