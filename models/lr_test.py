#!/usr/bin/env python
# coding: utf-8

from data import TickerCached as Ticker
from sklearn.linear_model import LogisticRegression
# Basic setup
import numpy as np
import pandas as pd


# %pip list
#!jupyter nbconvert --to script lr_test.ipynb
# get_ipython().run_line_magic('matplotlib', 'inline')


## Load Nasdaq summary of Symbols

nasdaq = pd.read_csv('nasdaqlisted.txt', delimiter='|')
print(nasdaq.head())


# ## Decide on training and validation sets


Ntotal = 10
Ntrain = 7

symbols = nasdaq['Symbol'].sample(Ntotal)

symbols_train = list(symbols[:Ntrain].values)
symbols_val= list(symbols[Ntrain:].values)

print( "Train symbols: ", symbols_train, '\n')
print( "Val symbols: ", symbols_val)


# ## Download and format historical data
# - download the data
# - generate features of interest and labels
# - concatenate into a large dataframe
# 


# import yfinance as yf
# from features import addFeatures


# In[10]:





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
    tickerDf['CloseFutureChange'] = tickerDf['CloseAvgDelayed'] - tickerDf['Close']

    # If the average is up at the delay, then good (else bad)
    tickerDf['Good'] = 0  # preset all bad
    tickerDf.loc[tickerDf['CloseFutureChange'] > 0, 'Good'] = 1

    # clean for return
    tickerDf.dropna(inplace=True)
    # tickerDf_updated = tickerDf
    return tickerDf


# ticker = yf.Ticker(symbols_train[0])
# tDF = ticker.history(period='1d', start='2010-1-1', end='2020-1-25')
# tDF.reset_index(inplace=True)


def getSymbolDF( symbols):
    ticker_df_list = []
    for tickerStr in symbols:
        ticker = Ticker(tickerStr)
        tDF = ticker.history(period='1d', start='2020-1-1', end='2021-8-25')
        #         tDF = ticker.history(period='1d', start='2010-1-1', end='2020-1-25')
        tDF = addFeatures(tDF)
        ticker_df_list.append(addFeatures(tDF) )
    
    df = pd.concat(ticker_df_list)        
    return df



trainDF = getSymbolDF( symbols_train )
valDF = getSymbolDF( symbols_val )

trainDF.to_pickle( 'train.pkl')
valDF.to_pickle( 'val.pkl')



trainDF


# ## Build a simple predictive model

# In[16]:






# clf = LogisticRegression(random_state=0).fit(X, y)
# clf.predict(X[:2, :])
# clf.predict_proba(X[:2, :])
# clf.score(X, y)


# In[27]:


feats = ["DailyChangeMean", "DailyChangeStd" ]
target = "Good"


# In[28]:


X = trainDF[feats]
y = trainDF[target]


# In[29]:


clf = LogisticRegression(random_state=0).fit(X, y)


# In[30]:


s = clf.score(X,y)
print( f"Training set accuracy: {s}")


# ## Check generalization

# In[31]:


X_val = valDF[feats]
y_val = valDF[target]


# In[32]:


s = clf.score(X_val,y_val)
print( f"Validation set accuracy: {s}")


# ## Visualize and Exploratory Data Analysis (EDA)
# 

# In[ ]:


trainDF['Good'].value_counts()


# In[ ]:




