import pandas as pd
import quandl
import datetime
import numpy as np

from log_quandl import *

import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY

# Log with quandl API key

log_quandl()

# Choose the date interval

startdate = datetime.date(2021,1,1)
mydate = datetime.date.today()

# Get the stock data for choosen companies
# https://www.quandl.com/data/EURONEXT-Euronext-Stock-
# Test the function map with a callback function
# Using re

def getQuandl(index):
    return quandl.get(index, start_date = startdate, end_date = mydate)

import re

codeQuandl = ["EURONEXT/GLE", "EURONEXT/BNP", "EURONEXT/ACA"]

stocks = list(map(getQuandl, codeQuandl))
print(stocks)
print(type(stocks))
print(type(stocks[1]))

fields = ["Open", "High", "Low", "Last"]
df = pd.DataFrame(index = stocks[1].index) # Empty Dataframe with the index of the stocks

title = "Cours "

# Test on dataframe
for i in range(len(stocks)):
    stocks[i] = stocks[i].loc[:,fields]
    crit_ticker = re.search("/", codeQuandl[i])
    ticker = codeQuandl[i][crit_ticker.span()[1]:len(codeQuandl[i])]
    df[ticker] = stocks[i]["Open"]
    title = title + ticker + " "

#http://python-simple.com/python-matplotlib/configuration-axes.php

plt.style.use("seaborn-dark")

fig, ax = plt.subplots()

fig.autofmt_xdate() # Rotate the legend automatically to have enought space

if df.index[-1] - df.index[0] < pd.Timedelta("730 days"):
    weekFormatter = DateFormatter('%b %d')
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()                  # minor ticks on the days

    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)

else:
    
    weekFormatter = DateFormatter('%b %d %Y')

ax.xaxis.set_major_formatter(weekFormatter)

plt.grid(True)

plt.title(title)
plt.plot(df) # df.plot work but for now this one works better

print(plt.style.available)

plt.tight_layout()

plt.show()
