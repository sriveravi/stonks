# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75


from data import Ticker2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from features import tickerDf  # some data

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)
