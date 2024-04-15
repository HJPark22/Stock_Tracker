from vars.config import API_KEY
from api.daily import return_daily_trades
from api.news import return_news


if __name__ == '__main__':
    #TSLA = return_daily_trades('TSLA', API_KEY)
    SYMBOL = input()
    new = return_news(SYMBOL,)
    print("Successful")