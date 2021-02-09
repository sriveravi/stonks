import os
import pandas as pd
import yfinance as yf


class Ticker2(yf.Ticker):
    def __init__(self, ticker='MSFT', savePath='someData.pkl'):
        super().__init__(ticker)
        self.savePath = savePath

    def history(self):
        return super().history(
            period='1d', start='2010-1-1', end='2020-1-25')

        # define the ticker symbol

        # get data on this ticker
        tickerData = yf.Ticker(self.tickerSymbol)

        # get the historical prices for this ticker
        if os.path.exists(self.savePath):
            tickerDf = pd.read_pickle(self.savePath)
        else:
            tickerDf = tickerData.history(
                period='1d', start='2010-1-1', end='2020-1-25')
            tickerDf.to_pickle(self.savePath)
        return tickerDf
