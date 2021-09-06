#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %pip list
# get_ipython().system('jupyter nbconvert --to script lr_test.ipynb')


# In[2]:


# Basic setup
import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# %pip install yfinance


# In[4]:


ls


# ## A few reminder examples of plotting and running a script

# In[5]:


# %matplotlib inline
# import numpy as np
# import matplotlib.pyplot as plt

# t = np.arange(0, 5, 0.2)
# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
# plt.show()


# In[6]:


# %run demo.py


# ## Load Nasdaq summary of Symbols

# In[7]:


nasdaq = pd.read_csv('nasdaqlisted.txt', delimiter='|')
print(nasdaq.head())


# ## Decide on training and validation sets

# In[48]:


Ntotal = 100
Ntrain = 70

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

# In[49]:


import yfinance as yf
# from features import addFeatures


# In[50]:





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


# In[51]:


# ticker = yf.Ticker(symbols_train[0])
# tDF = ticker.history(period='1d', start='2010-1-1', end='2020-1-25')
# tDF.reset_index(inplace=True)


# In[52]:



# tDF


# In[ ]:





# In[53]:


def getSymbolDF( symbols):
    ticker_df_list = []
    for tickerStr in symbols:
        ticker = yf.Ticker(tickerStr)
        tDF = ticker.history(period='1d', start='2020-1-1', end='2021-8-25')
        #         tDF = ticker.history(period='1d', start='2010-1-1', end='2020-1-25')
        tDF = addFeatures(tDF)
        ticker_df_list.append(addFeatures(tDF) )
    
    df = pd.concat(ticker_df_list)        
    return df


# In[54]:


trainDF = getSymbolDF( symbols_train )
valDF = getSymbolDF( symbols_val )

trainDF.to_pickle( 'train.pkl')
valDF.to_pickle( 'val.pkl')


# In[57]:


trainDF


# ## Build a simple predictive model

# In[58]:


from sklearn.linear_model import LogisticRegression



# clf = LogisticRegression(random_state=0).fit(X, y)
# clf.predict(X[:2, :])
# clf.predict_proba(X[:2, :])
# clf.score(X, y)


# In[59]:


feats = ["DailyChangeMean", "DailyChangeStd","CloseFutureChange" ]
target = "Good"


# In[64]:


X = trainDF[feats]
y = trainDF[target]


# In[65]:


clf = LogisticRegression(random_state=0).fit(X, y)


# In[67]:


s = clf.score(X,y)
print( f"Training set accuracy: {s}")


# ## Check generalization

# In[68]:


X_val = valDF[feats]
y_val = valDF[target]


# In[70]:


s = clf.score(X_val,y_val)
print( f"Validation set accuracy: {s}")


# ## Visualize and Exploratory Data Analysis (EDA)
# 

# In[ ]:




