from vars.config import API_KEY_AV, API_KEY_P
from api.daily import return_daily_trades, aggregate_stats
from api.news import symbols_to_api
from api.news import return_news
from vars.file_location import current_csv, past_csv
from test_.backtest import test_past, test_current
from utils.helpers import combine_cur_stocks_news, combine_past_stocks_news, return_df
import pandas as pd
import numpy as np
import os


if __name__ == "__main__":
    SYMBOL = "NVDA"
    time = test_current(year=2024, month=04, day=20, hour=12, minute=00, diff_days=60)
    temp = return_news(
        SYMBOL, API_KEY_AV, time["news_START_DATE"], time["news_END_DATE"]
    )
    df = return_df(time)
    for top_stock in temp["Ticker"].values:
        if top_stock.isalpha():
            current = aggregate_stats(
                return_daily_trades(
                    top_stock, API_KEY_P, time["stock_END_DATE"], time["current_DATE"]
                )
            )
            if time["Current"]:
                df = pd.concat(
                    [
                        df if not df.empty else None,
                        combine_cur_stocks_news(
                            top_stock,
                            current,
                            temp[temp.Ticker == top_stock]["Score"].values[0],
                        ),
                    ],
                    ignore_index=True,
                )
            else:
                past = aggregate_stats(
                    return_daily_trades(
                        top_stock,
                        API_KEY_P,
                        time["stock_START_DATE"],
                        time["stock_END_DATE"],
                    )
                )
                df = pd.concat(
                    [
                        df if not df.empty else None,
                        combine_past_stocks_news(
                            top_stock,
                            past,
                            current,
                            temp[temp.Ticker == top_stock]["Score"].values[0],
                        ),
                    ],
                    ignore_index=True,
                )
    df.sort_values(by="Score", ascending=False, inplace=True)
    if os.path.getsize(past_csv):
        df.to_csv(past_csv, index=False)
    else:
        df.to_csv(past_csv, mode="a", index=False, header=False)
