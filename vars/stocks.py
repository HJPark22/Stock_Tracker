from datetime import datetime, timedelta

# Get today's date
today = datetime.today()

# Subtract one day from today's date
one_day_earlier = (today - timedelta(days=1)).strftime("%Y-%m-%d")

one_year_earlier = (today - timedelta(days=365)).strftime("%Y-%m-%d")

