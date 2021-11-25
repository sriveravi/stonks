import os
import pandas as pd
import yfinance as yf


class TickerCached(yf.Ticker):
    def __init__(self, *args, ticker='MSFT', **kwargs):
        super().__init__(*args, ticker, **kwargs, )
        saveDir = 'TickerData'
        os.makedirs( saveDir, exist_ok=True)
        self.savePath = os.path.join(saveDir, ticker +'.pkl')

    def history(self, *args, **kwargs):
        if os.path.exists(self.savePath):
            tickerDf = pd.read_pickle(self.savePath)
        else:
            # tickerDf = super().history(*args, **kwargs)
            tickerDf = yf.Ticker(self.ticker).history(*args, **kwargs)
            tickerDf.to_pickle(self.savePath)
        return tickerDf
