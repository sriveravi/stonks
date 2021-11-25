#!/usr/bin/env python
# coding: utf-8

from data import TickerCached as Ticker
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from features import getSymbolDF

# --------   DATA  -----------------

## Load Nasdaq summary of Symbols
nasdaq = pd.read_csv('nasdaqlisted.txt', delimiter='|')
# print(nasdaq.head())

# Decide on training and validation sets
Ntotal = 10
Ntrain = 7

symbols = nasdaq['Symbol'].sample(Ntotal)
symbols_train = list(symbols[:Ntrain].values)
symbols_val= list(symbols[Ntrain:].values)
print( "Train symbols: ", symbols_train, '\n')
print( "Val symbols: ", symbols_val)


timeParams = {'period':'1d', 'start':'2020-1-1', 'end':'2021-8-25'}


# ## Download and format historical data
trainDF = getSymbolDF( symbols_train, **timeParams)
valDF = getSymbolDF( symbols_val, **timeParams )

# trainDF.to_pickle( 'train.pkl')
# valDF.to_pickle( 'val.pkl')


# -----------  MODELING ----------------
# ## Build a simple predictive model

# clf = LogisticRegression(random_state=0).fit(X, y)
# clf.predict(X[:2, :])
# clf.predict_proba(X[:2, :])
# clf.score(X, y)

feats = ["DailyChangeMean", "DailyChangeStd" ]
target = "Good"

# fit model
X = trainDF[feats]
y = trainDF[target]
clf = LogisticRegression(random_state=0).fit(X, y)
s = clf.score(X,y)
print( f"Training set accuracy: {s}")

# Check generalization
X_val = valDF[feats]
y_val = valDF[target]
s = clf.score(X_val,y_val)
print( f"Validation set accuracy: {s}")

# ## Visualize and Exploratory Data Analysis (EDA)
print('Class counts:')
trainDF['Good'].value_counts()

