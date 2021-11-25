import os
import pandas as pd
import yfinance as yf


class TickerCached(yf.Ticker):
    def __init__(self, ticker='MSFT'):
        super().__init__(ticker)
        saveDir = 'TickerData'
        os.makedirs( saveDir, exist_ok=True)
        self.savePath = os.path.join(saveDir, ticker +'.pkl')

    def history(self, *args, **kwargs):
        if os.path.exists(self.savePath):
            tickerDf = pd.read_pickle(self.savePath)
        else:
            tickerDf = super().history(*args, **kwargs)
            # tickerDf = yf.Ticker(self.ticker).history(*args, **kwargs)
            tickerDf.to_pickle(self.savePath)
        return tickerDf




# get data on this ticker
tickerSymbol = 'MSFT'
tickerData = TickerCached(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2021-1-1', end='2021-6-25')