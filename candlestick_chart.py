import pandas as pd
import quandl
import datetime
from log_quandl import *

### Récupérer les données avec Quandl

log_quandl()

# Choix des de l'intervalle de date
startdate = datetime.date(2021,1,1)
mydate = datetime.date.today()

# Récupérer le nom des series directement sur le site quandl
codeQuandl = "EURONEXT/GLE"
data = quandl.get(codeQuandl, start_date=startdate, end_date=mydate)

### Visualisation of market data (Graphique simple)

"""
import matplotlib.pyplot as plt

print(str(mydate))

data["Last"].plot(grid = True, figsize = (12,7), title = "Exemple")
plt.show()
"""

### Visualisation of market data (Japanese candlestick)

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
import mplfinance as mpf

# With mplfinance

if "Last" in data.columns:
    data = data.rename(columns = {"Last" : "Close"}) # Change the name of the variable "Last" in "Close"

"""
mpf.plot(data,type='candle')
"""

# Function

def pandas_candlestick_ohlc(dat, stick = "day"):

    mondays = WeekdayLocator(MONDAY) # 
    alldays = DayLocator()
    weekFormatter = DateFormatter('%b %d %d')
    dayFormatter = DateFormatter('%d')

    fields = ["Open", "High", "Low", "Close"]
    transdat = dat.loc[:,fields]
    
    if (type(stick)==str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used to plot
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x : x.isocalendar()[1]) # Identifie les semaines
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x : x.month) # Identifie les mois
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x : x.isocalendar()[0]) # Identifie les années
        
            grouped = transdat.groupby(list(set(["year", stick]))) # Group by year and the choice
            print(type(grouped))

            plotdat = pd.DataFrame({"Open" : [], "High": [], "Low" : [], "Close": []}) # New dataFrame with the data by weeks/months/years

            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open" : group.iloc[0,0], "High" : max(group.High), 
                                "Low" : min(group.Low), "Close" : group.iloc[-1,3]},
                                index = [group.index[0]])) # We use DataFrame instead of dictionary to define the index

        else : 
            raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year" or a positive integer')
    
    # Set plot parameters, including the axis object ax used for plotting

    # Create the candlestick chart taking the time slot to adjuste colors
    # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb


    alines_dates = [i.date() for i in plotdat.index]
    alines_open = [i for i in plotdat["Open"]]
    alines_close = [i for i in plotdat["Close"]]
    
    alines_values = []

    for i in range(len(alines_dates)):
        alines_values.append((alines_dates[i], (alines_close[i] + alines_open[i])/ 2))

    import time

    t = time.localtime()
    h = int(time.strftime("%H",t))
    if h in [i + 20 for i in range(4)] or h in [i for i in range(9)]:
        customcolor = mpf.make_marketcolors(up = "#75BA74", down = "#B97C7C", inherit = True)
        s = mpf.make_mpf_style(base_mpf_style = "nightclouds", marketcolors = customcolor)
        mpf.plot(plotdat,type='candle', style = s, alines = dict(alines=alines_values, colors=['w'], linewidths=1, alpha=0.68))
    else :
        mpf.plot(plotdat,type='candle', style = 'yahoo')

    # print(mpf.available_styles())
    
    # Create the candlestick with plotly.graph_object

    """
    import plotly.graph_objects as go

    candlestick = go.Candlestick(
                            x=plotdat.index,
                            open=plotdat['Open'],
                            high=plotdat['High'],
                            low=plotdat['Low'],
                            close=plotdat['Close']
                            )

    fig = go.Figure(data=[candlestick])

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()
    """

pandas_candlestick_ohlc(data, stick = "day")




