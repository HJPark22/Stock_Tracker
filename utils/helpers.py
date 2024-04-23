import pandas as pd
import numpy as np


def create_cur_df():
    df = pd.DataFrame(
        columns=[
            "Ticker",
            "Score",
            "hist_price",
            "current_change",
            "current_price",
            "avg_vol",
        ]
    )
    return df.copy()


def create_past_df():
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
    return df.copy()


def combine_past_stocks_news(SYMBOL, past, current, score):
    """Combine past and current to create df"""
    cur = pd.DataFrame(
        [
            {
                "Ticker": SYMBOL,
                "Score": round(score, 3),
                "initial_price": past[0],
                "hist_change": round(past[2], 3),
                "hist_price": past[1],
                "current_change": round(current[2], 3),
                "current_price": current[1],
                "avg_vol": round(np.mean([past[3], current[3]]), 0),
            }
        ]
    )
    return cur


def combine_cur_stocks_news(SYMBOL, current, score):
    """Combine current to create df"""
    cur = pd.DataFrame(
        [
            {
                "Ticker": SYMBOL,
                "Score": round(score, 3),
                "hist_price": current[0],
                "current_change": round(current[2], 3),
                "current_price": current[1],
                "avg_vol": round(current[3], 0),
            }
        ]
    )
    return cur


def return_df(time_object):
    if time_object["Current"]:
        df = create_cur_df()
    else:
        df = create_past_df()
    return df.copy()
