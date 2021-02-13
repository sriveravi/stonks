# Notes: basic yfinance demo mostly taken from:
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75


from data import Ticker2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from features import tickerDf_updated as data  # some data
import pymc3 as pm


def plot_traces(traces, model, retain=0):
    """
    Convenience function:
    Plot traces with overlaid means and values
    """
    with model:
        ax = pm.traceplot(
            traces[-retain:],
            lines=tuple([(k, {}, v["mean"])
                         for k, v in pm.summary(traces[-retain:]).iterrows()]),
        )

        for i, mn in enumerate(pm.summary(traces[-retain:])["mean"]):
            ax[i, 0].annotate(
                f"{mn:.2f}",
                xy=(mn, 0),
                xycoords="data",
                xytext=(5, 10),
                textcoords="offset points",
                rotation=90,
                va="bottom",
                fontsize="large",
                color="#AA0022",
            )


# sns.set_style('darkgrid')
sns.set_theme(style='darkgrid', font_scale=1.5)


data.dropna(inplace=True)
print(data.columns)


# # actual model stuff
# with pm.Model() as baseModel:

#     # Independent parameters for each county
#     a = pm.Normal("a", 0, sigma=100, shape=1)
#     b = pm.Normal("b", 0, sigma=100, shape=1)

#     # Model error
#     eps = pm.HalfCauchy("eps", 5)

#     # Model prediction of radon level
#     # a[county_idx] translates to a[0, 0, 0, 1, 1, ...],
#     # we thus link multiple household measures of a county
#     # to its coefficients.
#     good_est = a + b * data.Volume.values

#     # Data likelihood
#     y = pm.Normal("y", good_est, sigma=eps, observed=data.Good)

with pm.Model() as logistic_model:
    pm.glm.GLM.from_formula(
        "Good ~ DailyChangeMean + DailyChangeStd", data, family=pm.glm.families.Binomial()
    )


with logistic_model:
    trace = pm.sample(
        1000, tune=1000, return_inferencedata=False, cores=1)


plot_traces(trace, logistic_model)
# plt.figure(figsize=(7, 7))
# pm.traceplot(trace)
plt.tight_layout()
