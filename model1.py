# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)

# define the ticker symbol
tickerSymbol = 'MSFT'
demoData = 'someData.pkl'


# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
if os.path.exists(demoData):
    tickerDf = pd.read_pickle(demoData)
else:
    tickerDf = tickerData.history(
        period='1d', start='2010-1-1', end='2020-1-25')
    tickerDf.to_pickle('someData.pkl')

# make Data a value you can work with
tickerDf.reset_index('Date', inplace=True)
# print(tickerDf.columns)
print(tickerDf.info())


# # make a nice little figure
# sns.lineplot(x='Date', y='Close', data=tickerDf)
# plt.title(tickerSymbol)

# -------------------------

df = tickerDf.groupby([pd.Grouper(key='Date', freq='W-MON')]
                      )  # weekly, mondays

print(f"Len of original DF: {len(tickerDf)}")
print(f"Len of groupby DF with some opration DF: {len(df.sum())}")


# tickerDf['growthSlope'] = tickerDf['Close'] - tickerDf['Open']
