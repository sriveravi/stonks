import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data import Ticker2
import os

figDir = 'Figs'
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

tickerDf.columns
tickerDf.head()

# -----
# features parameters
closingRollAvgInterval_D = 7
dailyChangeRollAvgInterval_D = 7


# --------
# daily change features
#   rolling average, rolling std.
tickerDf['DailyChange'] = tickerDf['Close'] - tickerDf['Open']
tickerDf['DailyChangeMean'] = tickerDf.rolling(
    f"{dailyChangeRollAvgInterval_D}D", on='Date')['DailyChange'].mean()
tickerDf['DailyChangeStd'] = tickerDf.rolling(
    f"{dailyChangeRollAvgInterval_D}D", on='Date')['DailyChange'].std()

# show it
plt.figure(figsize=(6, 8))
plt.subplot(2, 1, 1)
# sns.barplot(x='Date', y='DailyChangeMean', data=tickerDf)
ax = sns.scatterplot(x='Date', y='DailyChangeMean', data=tickerDf)
ax.axhline(0, linestyle='-', color='red')
ax.set_xticklabels([])
ax.set_xlabel('')
ax.set_ylabel(f'[C-O] Mean (Roll {dailyChangeRollAvgInterval_D} D)')

plt.subplot(2, 1, 2)
ax = sns.scatterplot(x='Date', y='DailyChangeStd', data=tickerDf)
ax.set_ylabel(f'[C-O] STD (Roll {dailyChangeRollAvgInterval_D} D)')


# ------
# closing mean features ( for estimating good/bad at a delay)
#   rolling average closing mean
tickerDf['CloseAvg'] = tickerDf.rolling(
    f"{closingRollAvgInterval_D}D", on='Date')['Close'].mean()

# show closing average rolling mean
plt.figure()
sns.lineplot(x='Date', y='value', hue='variable',
             data=pd.melt(tickerDf, id_vars=['Date'], value_vars=['Close', 'CloseAvg']))
plt.title(tickerSymbol)

# -------------------------
# Time delay of moving average closing
#   For identifying good/bad

delay = -14  # days
tickerDf['CloseAvgDelayed'] = tickerDf['CloseAvg'].shift(
    periods=delay, fill_value=np.nan)
tickerDf['CloseFutureChange'] = tickerDf['CloseAvgDelayed'] - tickerDf['Close']

# If the average is up at the delay, then good (else bad)
tickerDf['Good'] = 0  # preset all bad
tickerDf.loc[tickerDf['CloseFutureChange'] > 0, 'Good'] = 1


plt.figure(figsize=(6, 8))
plt.subplot(3, 1, 1)
# plt.plot(tickerDf['Date'], tickerDf['Close'], '-')
ax = sns.lineplot(x='Date', y='Close', data=tickerDf)
ax.set_xticklabels([])
ax.set_xlabel('')

plt.subplot(3, 1, 2)
# plt.plot(tickerDf['Date'], tickerDf['CloseFutureChange'], '.')
ax = sns.scatterplot(x='Date', y='CloseFutureChange', data=tickerDf)
ax.axhline(0, linestyle='-', color='red')
ax.set_xticklabels([])
ax.set_xlabel('')
plt.ylabel(f'{-1*delay} day change')

plt.subplot(3, 1, 3)
# plt.plot(tickerDf['Date'], tickerDf['Good'], '.')
# ax = sns.scatterplot(x='Date', y='Good', data=tickerDf, markers='+')
kwargs = {"alpha": 1.0, "s": 2}  # "color": "darkred",
ax = sns.scatterplot(x='Date', y='Good', data=tickerDf, **kwargs)
plt.yticks([0, 1], ["No", "Yes"])
plt.suptitle(tickerSymbol)
# tickerDf
# tickerDf.dropna(inplace=True)


# -------------------------
# show some relationships between variables of interest

# print(tickerDf.columns)

colsOfInterest = ['Volume', 'DailyChange', 'DailyChangeMean',
                  'DailyChangeStd', 'CloseFutureChange', 'Good']

sns.pairplot(tickerDf[colsOfInterest])

# ---------------------------
# Visualize the good and bad by 2 features
plt.figure()

sns.scatterplot(x='DailyChangeMean', y='DailyChangeStd',
                hue='Good', data=tickerDf)
plt.title(tickerSymbol)


# df = tickerDf.groupby([pd.Grouper(key='Date', freq='W-MON')]
#                       )  # weekly, mondays

# print(f"Len of original DF: {len(tickerDf)}")
# print(f"Len of groupby DF with some opration DF: {len(df.sum())}")


# iterator = iter(df)
# idx, subdf = next(iterator)


# subdf
