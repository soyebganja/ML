# -*- coding: utf-8 -*-
"""13.2:Feature Selection Using Correlation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15NLALEHAlHlnTMUecz9M0qVtNthcZ6KY
"""

import pandas as pd

df = pd.read_csv('home_prices.csv')
df.head()

df.color.unique()

df_encoded = pd.get_dummies(df, columns=["color"], drop_first=True)
df_encoded.head()

cm = df_encoded.corr()
cm

cm_price = abs(cm['price_lakhs'])
cm_price

selected_features = cm_price[cm_price > 0.2].index.drop('price_lakhs')
selected_features

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X = df_encoded[selected_features]
y = df_encoded['price_lakhs']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("R-squared:", r2, ", Mean Squared Error:", mse)

