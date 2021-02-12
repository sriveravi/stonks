import os
import pandas as pd
import yfinance as yf


class Ticker2(yf.Ticker):
    def __init__(self, ticker='MSFT', savePath='someData.pkl'):
        super().__init__(ticker)
        self.savePath = savePath

    def history(self, *args, **kwargs):
        if os.path.exists(self.savePath):
            tickerDf = pd.read_pickle(self.savePath)
        else:
            tickerDf = super().history(*args, **kwargs)
            tickerDf.to_pickle(self.savePath)
        return tickerDf
