import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)

# define the ticker symbol
tickerSymbol = 'MSFT'

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')

# see your data
tickerDf


print(tickerDf.columns)
sns.lineplot(x='Date', y='Close', data=tickerDf)
plt.title(tickerSymbol)
