import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from data import TickerCached as Ticker




def addFeatures( tickerDf, closingRollAvgInterval_D = 7, 
                 dailyChangeRollAvgInterval_D = 7, delay = -14):  # days):

    #     delay in days, negative value 

    # make Data a value you can work with
    tickerDf.reset_index(inplace=True)

    # --------
    # daily change features
    #   rolling average, rolling std.
    tickerDf['DailyChange'] = tickerDf['Close'] - tickerDf['Open']
    tickerDf['DailyChangeMean'] = tickerDf.rolling(
        f"{dailyChangeRollAvgInterval_D}D", on='Date')['DailyChange'].mean()
    tickerDf['DailyChangeStd'] = tickerDf.rolling(
        f"{dailyChangeRollAvgInterval_D}D", on='Date')['DailyChange'].std()


    # ------
    # closing mean features ( for estimating good/bad at a delay)
    #   rolling average closing mean
    tickerDf['CloseAvg'] = tickerDf.rolling(
        f"{closingRollAvgInterval_D}D", on='Date')['Close'].mean()


    # -------------------------
    # Time delay of moving average closing
    #   For identifying good/bad


    tickerDf['CloseAvgDelayed'] = tickerDf['CloseAvg'].shift(
        periods=delay, fill_value=np.nan)
    tickerDf['truth_closeChange'] = tickerDf['CloseAvgDelayed'] - tickerDf['Close']

    # If the average is up at the delay, then good (else bad)
    tickerDf['Good'] = 0  # preset all bad
    tickerDf.loc[tickerDf['truth_closeChange'] > 0, 'Good'] = 1

    # clean for return
    tickerDf.dropna(inplace=True)
    # tickerDf_updated = tickerDf
    return tickerDf


def getSymbolDF( symbols, **kwargs):
    ticker_df_list = []
    for tickerStr in symbols:
        try:
            ticker = Ticker(tickerStr)
            tDF = ticker.history(**kwargs)
            #         tDF = ticker.history(period='1d', start='2010-1-1', end='2020-1-25')
            tDF = addFeatures(tDF)
            ticker_df_list.append(addFeatures(tDF) )
        except:
            print(f'Error getting {tickerStr}')

    df = pd.concat(ticker_df_list)        
    return df

tickerSymbol = 'MSFT'
tickerData = Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')
tickerDf_updated =  addFeatures( tickerDf)


# df = tickerDf.groupby([pd.Grouper(key='Date', freq='W-MON')]
#                       )  # weekly, mondays

# print(f"Len of original DF: {len(tickerDf)}")
# print(f"Len of groupby DF with some opration DF: {len(df.sum())}")


# iterator = iter(df)
# idx, subdf = next(iterator)


# subdf
if __name__ == '__main__':

    figDir = 'Figs'
    sns.set_theme(style='darkgrid', font_scale=1.5)

    # print(tickerDf.columns)
    print(tickerDf.info())

    # # make a nice little figure
    # sns.lineplot(x='Date', y='Close', data=tickerDf)
    # plt.title(tickerSymbol)

    print(tickerDf.columns)

    # ------------------
    # show it daily change mean and stev
    plt.figure(figsize=(6, 8))
    plt.subplot(2, 1, 1)
    ax = sns.scatterplot(x='Date', y='DailyChangeMean', data=tickerDf)
    ax.axhline(0, linestyle='-', color='red')
    ax.set_xticklabels([])
    ax.set_xlabel('')
    # ax.set_ylabel(f'[C-O] Mean (Roll {dailyChangeRollAvgInterval_D} D)')
    plt.subplot(2, 1, 2)
    ax = sns.scatterplot(x='Date', y='DailyChangeStd', data=tickerDf)
    # ax.set_ylabel(f'[C-O] STD (Roll {dailyChangeRollAvgInterval_D} D)')

    # show closing average rolling mean
    plt.figure()
    sns.lineplot(x='Date', y='value', hue='variable',
                 data=pd.melt(tickerDf, id_vars=['Date'], value_vars=['Close', 'CloseAvg']))
    plt.title(tickerSymbol)

    # ------------------
    # plot close, X day change, Good
    plt.figure(figsize=(6, 8))
    plt.subplot(3, 1, 1)
    # plt.plot(tickerDf['Date'], tickerDf['Close'], '-')
    ax = sns.lineplot(x='Date', y='Close', data=tickerDf)
    ax.set_xticklabels([])
    ax.set_xlabel('')

    plt.subplot(3, 1, 2)
    # plt.plot(tickerDf['Date'], tickerDf['truth_closeChange'], '.')
    ax = sns.scatterplot(x='Date', y='truth_closeChange', data=tickerDf)
    ax.axhline(0, linestyle='-', color='red')
    ax.set_xticklabels([])
    ax.set_xlabel('')
    # plt.ylabel(f'{-1*delay} day change')

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
    colsOfInterest = ['Volume', 'DailyChange', 'DailyChangeMean',
                      'DailyChangeStd', 'truth_closeChange', 'Good']

    sns.pairplot(tickerDf[colsOfInterest])

    # ---------------------------
    # Visualize the good and bad by 2 features
    plt.figure()
    sns.scatterplot(x='DailyChangeMean', y='DailyChangeStd',
                    hue='Good', data=tickerDf)
    plt.title(tickerSymbol)
