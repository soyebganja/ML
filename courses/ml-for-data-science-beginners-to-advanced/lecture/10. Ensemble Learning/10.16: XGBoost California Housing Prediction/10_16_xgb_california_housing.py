# -*- coding: utf-8 -*-
"""10.16:XGBoost: California Housing Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S1BuZCnuoRlseGM7LRP6GLtvYozYwWNI
"""

import pandas as pd
from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing()

print(housing.data.shape, housing.target.shape)
print(housing.feature_names[0:6])

df = pd.DataFrame(housing.data, columns=housing.feature_names)
df.head()

housing.target

df["MedHouseVal"] = housing.target
df.head()

df.isnull().sum()

df.describe()

from sklearn.model_selection import train_test_split
x = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

"""### Train a model using Linear Regression"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import time

start = time.time()
model_LR = LinearRegression()
model_LR.fit(X_train, y_train)
end = time.time()

y_pred = model_LR.predict(X_test)

r2s_LR = r2_score(y_test, y_pred)
mse_LR = mean_squared_error(y_test, y_pred)

print("R2 Score: ", r2s_LR, " MSE: ", mse_LR, " Time taken: ", end-start)

"""### Train a model using Gradient Boosting(GBM)"""

from sklearn.ensemble import GradientBoostingRegressor

start = time.time()
model_GBM = GradientBoostingRegressor()
model_GBM.fit(X_train, y_train)
end = time.time()

y_pred = model_GBM.predict(X_test)

r2s_GBM = r2_score(y_test, y_pred)
mse_GBM = mean_squared_error(y_test, y_pred)

print("R2 Score: ", r2s_GBM, " MSE: ", mse_GBM, " Time taken: ", end-start)

"""### Train a model using XGradient Boosting(XGB)"""

import xgboost as xgb

start = time.time()
model_XGB = xgb.XGBRegressor()
model_XGB.fit(X_train, y_train)
end = time.time()

y_pred = model_XGB.predict(X_test)

r2s_XGB = r2_score(y_test, y_pred)
mse_XGB = mean_squared_error(y_test, y_pred)

print("R2 Score: ", r2s_XGB, " MSE: ", mse_XGB, " Time taken: ", end-start)

