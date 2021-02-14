# Model 2
import numpy as np
import pymc3 as pm
from features import tickerDf_updated as data


Y_obs = data['Good'].values
X = data[['DailyChangeMean', 'DailyChangeStd']].values
num_covariates = X.shape[1]

with pm.Model() as model:
    alpha = pm.Normal("alpha", mu=0, sigma=10)
    beta = pm.Normal("beta", mu=0, sigma=10, shape=num_covariates)

    p = 1 / (
        1 + np.exp(alpha + pm.math.dot(X, beta))  # beta[0] * X1 + beta[1] * X2
    )

    # n is number Bernoulli trials
    Y = pm.Binomial('Y', n=1, p=p, observed=Y_obs)


# with Model() as model:  # model specifications in PyMC3 are wrapped in a with-statement
#     # Define priors
#     sigma = HalfCauchy("sigma", beta=10, testval=1.0)
#     intercept = Normal("Intercept", 0, sigma=20)
#     x_coeff = Normal("x", 0, sigma=20)


# a = np.array([[1, 0],
#               [0, 1]])
# b = np.array([[4, 1],
#               [2, 2]])
# np.matmul(a, b)
# np.dot( a,b)


# with basic_model:

#     # Priors for unknown model parameters
#     alpha = pm.Normal("alpha", mu=0, sigma=10)
#     beta = pm.Normal("beta", mu=0, sigma=10, shape=2)
#     sigma = pm.HalfNormal("sigma", sigma=1)

#     # Expected value of outcome
#     mu = alpha + beta[0] * X1 + beta[1] * X2

#     # Likelihood (sampling distribution) of observations
#     Y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=Y)
