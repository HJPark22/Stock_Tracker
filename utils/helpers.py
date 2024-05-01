import pandas as pd
import numpy as np
import os


def create_cur_df():
    df = pd.DataFrame(
        columns=[
            "Ticker",
            "Score",
            "hist_price",
            "current_trend",
            "current_price",
            "avg_vol",
            "roe_avg",
            "roe_trend",
            "roic_avg",
            "roic_trend",
            "earningsYield_avg",
            "earningsYield_trend",
            "freeCashFlowYield_avg",
            "freeCashFlowYield_trend",
            "debtToEquity_avg",
            "debtToEquity_trend",
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
            "current_trend",
            "current_price",
            "avg_vol",
            "roe_avg",
            "roe_trend",
            "roic_avg",
            "roic_trend",
            "earningsYield_avg",
            "earningsYield_trend",
            "freeCashFlowYield_avg",
            "freeCashFlowYield_trend",
            "debtToEquity_avg",
            "debtToEquity_trend",
        ]
    )
    return df.copy()


def combine_past_stocks_news(SYMBOL, past, current, metrics, score):
    """Combine past and current to create df"""
    cur = pd.DataFrame(
        [
            {
                "Ticker": SYMBOL,
                "Score": round(score, 3),
                "initial_price": past[0],
                "hist_trend": round(past[2], 3),
                "hist_price": past[1],
                "current_trend": round(current[2], 3),
                "current_price": current[1],
                "avg_vol": round(np.mean([past[3], current[3]]), 0),
                "roe_avg": round(metrics["roe_avg"], 2),
                "roe_trend": round(metrics["roe_trend"], 2),
                "roic_avg": round(metrics["roic_avg"], 2),
                "roic_trend": round(metrics["roic_trend"], 2),
                "earningsYield_avg": round(metrics["earningsYield_avg"], 2),
                "earningsYield_trend": round(metrics["earningsYield_trend"], 2),
                "freeCashFlowYield_avg": round(metrics["freeCashFlowYield_avg"], 2),
                "freeCashFlowYield_trend": round(metrics["freeCashFlowYield_trend"], 2),
                "debtToEquity_avg": round(metrics["debtToEquity_avg"], 2),
                "debtToEquity_trend": round(metrics["debtToEquity_trend"], 2),
            }
        ]
    )
    return cur


def combine_cur_stocks_news(SYMBOL, current, metrics, score):
    """Combine current to create df"""
    cur = pd.DataFrame(
        [
            {
                "Ticker": SYMBOL,
                "Score": round(score, 3),
                "hist_price": current[0],
                "current_trend": round(current[2], 3),
                "current_price": current[1],
                "avg_vol": round(current[3], 0),
                "roe_avg": round(metrics["roe_avg"], 2),
                "roe_trend": round(metrics["roe_trend"], 2),
                "roic_avg": round(metrics["roic_avg"], 2),
                "roic_trend": round(metrics["roic_trend"], 2),
                "earningsYield_avg": round(metrics["earningsYield_avg"], 2),
                "earningsYield_trend": round(metrics["earningsYield_trend"], 2),
                "freeCashFlowYield_avg": round(metrics["freeCashFlowYield_avg"], 2),
                "freeCashFlowYield_trend": round(metrics["freeCashFlowYield_trend"], 2),
                "debtToEquity_avg": round(metrics["debtToEquity_avg"], 2),
                "debtToEquity_trend": round(metrics["debtToEquity_trend"], 2),
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
