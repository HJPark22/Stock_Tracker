from datetime import datetime, timedelta

"""attempt to test 1"""

"""news_START_DATE = "20240417T0001"
news_END_DATE = "20240422T0001"
stock_START_DATE = "2024-02-15"
stock_END_DATE = "2024-03-16"
current_DATE = "2024-04-19"  """


def news_format(datetime_object):
    return datetime_object.strftime("%Y%m%dT%H%M")


def stock_format(datetime_object):
    return datetime_object.strftime("%Y-%m-%d")


def test_past(year, month, day, hour, minute, diff_days=60):
    current_datetime = datetime(
        year=year, month=month, day=day, hour=hour, minute=minute
    )
    future_datetime = current_datetime + timedelta(days=diff_days)
    past_datetime = current_datetime - timedelta(days=diff_days)

    d = {}
    d["news_START_DATE"] = news_format(current_datetime - timedelta(days=5))
    d["news_END_DATE"] = news_format(current_datetime)
    d["stock_START_DATE"] = stock_format(past_datetime)
    d["stock_END_DATE"] = stock_format(current_datetime)
    d["current_DATE"] = stock_format(future_datetime)
    d["Current"] = 0
    return d.copy()


def test_current(year, month, day, hour, minute, diff_days=60):
    current_datetime = datetime(
        year=year, month=month, day=day, hour=hour, minute=minute
    )
    past_datetime = current_datetime - timedelta(days=diff_days)

    d = {}
    d["news_START_DATE"] = news_format(current_datetime - timedelta(days=5))
    d["news_END_DATE"] = news_format(current_datetime)
    d["stock_END_DATE"] = stock_format(past_datetime)
    d["current_DATE"] = stock_format(current_datetime)
    d["Current"] = 1
    return d.copy()
