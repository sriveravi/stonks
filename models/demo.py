# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)

# define the ticker symbol
tickerSymbol = 'MSFT'

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')

# see your data
tickerDf

# make a nice little figure
print(tickerDf.columns)
sns.lineplot(x='Date', y='Close', data=tickerDf)
plt.title(tickerSymbol)
plt.ion()
plt.show()
plt.pause(1)
plt.close()


# ---------
# info on the company
print(tickerData.info)

# get event data for ticker
print(tickerData.calendar)

# get recommendation data for ticker
print(tickerData.recommendations)
