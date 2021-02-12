# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75


from data import Ticker2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from features import tickerDf_updated as tickerDf  # some data
import pymc3 as pm

# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)


tickerDf.dropna(inplace=True)


# actual model stuff
with pm.Model() as baseModel:

    # Independent parameters for each county
    a = pm.Normal("a", 0, sigma=100, shape=1)
    b = pm.Normal("b", 0, sigma=100, shape=1)

    # Model error
    eps = pm.HalfCauchy("eps", 5)

    # Model prediction of radon level
    # a[county_idx] translates to a[0, 0, 0, 1, 1, ...],
    # we thus link multiple household measures of a county
    # to its coefficients.
    radon_est = a + b * tickerDf.Volume.values

    # Data likelihood
    y = pm.Normal("y", radon_est, sigma=eps, observed=data.log_radon)


with baseModel:
    unpooled_trace = pm.sample(2000)
