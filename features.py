import pandas as pd
from data import Ticker2


tickerSymbol = 'MSFT'
tickerData = Ticker2(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')


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
