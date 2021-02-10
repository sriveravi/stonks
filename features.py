import pandas as pd
import numpy as np
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
avgIntDays = 7
tickerDf['CloseAvg'] = tickerDf.rolling(
    f"{avgIntDays}D", on='Date')['Close'].mean()

# show it
sns.lineplot(x='Date', y='value', hue='variable',
             data=pd.melt(tickerDf, id_vars=['Date'], value_vars=['Close', 'CloseAvg']))
plt.title(tickerSymbol)

# -------------------------
# Time delay of moving average closing
delay = -14  # days
tickerDf['CloseAvgDelayed'] = tickerDf['CloseAvg'].shift(
    periods=delay, fill_value=np.nan)
tickerDf['CloseFutureChange'] = tickerDf['CloseAvgDelayed'] - tickerDf['Close']

# If the average is up at the delay, then good (else bad)
tickerDf['Good'] = 0  # preset all bad
tickerDf.loc[tickerDf['CloseFutureChange'] > 0, 'Good'] = 1


plt.figure(figsize=(6, 8))
plt.subplot(3, 1, 3)
plt.plot(tickerDf['Date'], tickerDf['Good'], '.')
plt.subplot(3, 1, 2)
plt.plot(tickerDf['Date'], tickerDf['CloseFutureChange'], '.')
plt.subplot(3, 1, 1)
plt.plot(tickerDf['Date'], tickerDf['Close'], '-')

# tickerDf
# tickerDf.dropna(inplace=True)


# tickerDf['CloseAvg'].shift(periods=3, fill_value=np.nan)

# -------------------------

df = tickerDf.groupby([pd.Grouper(key='Date', freq='W-MON')]
                      )  # weekly, mondays

print(f"Len of original DF: {len(tickerDf)}")
print(f"Len of groupby DF with some opration DF: {len(df.sum())}")


iterator = iter(df)
idx, subdf = next(iterator)


subdf
