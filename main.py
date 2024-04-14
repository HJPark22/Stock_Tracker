from vars.config import API_KEY
from api.daily import return_daily_trades



if __name__ == '__main__':
    TSLA = return_daily_trades('TSLA', API_KEY)
    print("Successful")

print(TSLA)

TSLA