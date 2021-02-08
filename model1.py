# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)

# define the ticker symbol
tickerSymbol = 'MSFT'

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')
# tickerDf.to_pickle( 'someData.pkl')
tickerDf = pd.read_pickle( 'someData.pkl')


# see your data
#tickerDf

# make a nice little figure
#print(tickerDf.columns)
#sns.lineplot(x='Date', y='Close', data=tickerDf)
#plt.title(tickerSymbol)


# ---------
# info on the company
#tickerData.info
#
# get event data for ticker
#tickerData.calendar
#
## get recommendation data for ticker
#tickerData.recommendations
