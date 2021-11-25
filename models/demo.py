# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

# import matplotlib
# matplotlib.use('Agg')


# import yfinance as yf
from data import TickerCached as Ticker
import seaborn as sns
import matplotlib.pyplot as plt


import os

outputDir = 'Figs_Demo'
os.makedirs(outputDir, exist_ok=True)

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)

# define the ticker symbol
tickerSymbol = 'MSFT'

# get data on this ticker
tickerData = Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2021-1-1', end='2021-6-25')

# see your data
print(tickerDf)
print(tickerDf.columns)


# make a nice little figure
plt.figure()
ax = sns.lineplot(x='Date', y='Close', data=tickerDf, )
ax.tick_params(axis='x', rotation=90)
plt.title(tickerSymbol)
plt.savefig( os.path.join( outputDir, f'{tickerSymbol}_history.png'), bbox_inches='tight')
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
