import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data import Ticker2


sns.set_theme(style='darkgrid', font_scale=1.5)


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


# -----
# rolling average

avgIntDays = 20
tickerDf['Close_Avg'] = tickerDf.rolling(
    f"{avgIntDays}D", on='Date')['Close'].mean()


# sns.lineplot(x='Date', y='Close', data=tickerDf)
# sns.lineplot(x='Date', y='Close_Avg', data=tickerDf)

sns.lineplot(x='Date', y='value', hue='variable',
             data=pd.melt(tickerDf, id_vars=['Date'], value_vars=['Close', 'Close_Avg']))
plt.title(tickerSymbol)

# -------------------------

df = tickerDf.groupby([pd.Grouper(key='Date', freq='W-MON')]
                      )  # weekly, mondays

print(f"Len of original DF: {len(tickerDf)}")
print(f"Len of groupby DF with some opration DF: {len(df.sum())}")


iterator = iter(df)
idx, subdf = next(iterator)


subdf
