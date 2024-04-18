from vars.config import API_KEY_AV, API_KEY_P
from api.daily import return_daily_trades, aggregate_data
from api.news import symbols_to_api
from api.news import return_news
from vars.stocks import one_day_earlier, one_year_earlier
from test_.backtest import news_START_DATE, news_END_DATE, stock_START_DATE, stock_END_DATE, current_DATE
import requests

#def combine_stocks_news(news):




if __name__ == '__main__':
    #result = return_news('TSLA', API_KEY_AV)
    #print(result)
    temp = return_news('TSLA', API_KEY_AV, news_START_DATE, news_END_DATE)
    for top_stock in temp:
        change = aggregate_data(return_daily_trades(top_stock, API_KEY_P, stock_START_DATE, stock_END_DATE))
        current = return_daily_trades(top_stock, API_KEY_P, current_DATE, current_DATE)
        print(f"The stock: {top_stock}\nThe past: {change}\nNow: {current}")