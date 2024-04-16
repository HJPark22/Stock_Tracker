from vars.config import API_KEY_AV, API_KEY_P
from api.daily import return_daily_trades
from api.news import symbols_to_api
from api.news import return_news
from vars.stocks import one_day_earlier, one_year_earlier
import requests

options = ['Daily', 'News']

if __name__ == '__main__':
    #TSLA = return_daily_trades('TSLA', API_KEY)
    '''print("Choose an option from below\n----------------------------------------\n")
    for idx, option in enumerate(options):
        print(f"Option {idx}: {option}\n")
    #new = return_news(SYMBOL,)
    print("Successful")'''
    sym = 'AAPL'
    API_KEY_AV = "Z0UT46BYLNOBVIZ3"
    temp = return_news(sym,API_KEY_AV)
    print(temp)
    #data = return_daily_trades('TSLA', API_KEY_P, one_year_earlier, one_day_earlier)
    #print(data)

