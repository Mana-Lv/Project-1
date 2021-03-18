import pandas as pd
import quandl
import datetime
import numpy as np
from log_quandl import *

### Log with quandl API key

log_quandl()

## Choose the date interval

startdate = datetime.date(2021,3,15)
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
stocks_df = pd.DataFrame()

fields = ["Open", "High", "Low", "Last"]

a = stocks[1].loc[:,fields]

# Test 
for i in range(len(codeQuandl)):
    stocks[i].loc[:,fields]
    a = re.search("/", codeQuandl[i])
    b = codeQuandl[i][a.span()[1]:len(codeQuandl[1])]
    stocks_df.append({b : stocks[1]["Open"]}, ignore_index=True)
    c = stocks_df.append({b : stocks[1]["Open"]}, ignore_index=True)
    print(c)


