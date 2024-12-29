# -*- coding: utf-8 -*-
"""11.6:K Fold Cross Validation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JxhzfjM5serQpAYdUkFAi6szUj2fYs7e
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=8,
    n_redundant=2,
    n_repeated=0,
    n_classes=2,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model_lr = LogisticRegression()
model_lr.fit(X_train, y_train)

y_pred = model_lr.predict(X_test)
print(classification_report(y_test, y_pred))

from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model_lr = LogisticRegression()
    model_lr.fit(X_train, y_train)
    print(model_lr.score(X_test, y_test))

    # y_pred = model_lr.predict(X_test)
    # print(classification_report(y_test, y_pred))

"""### Evaluate Logistic Regression"""

from sklearn.model_selection import cross_val_score

scores_lg = cross_val_score(LogisticRegression(), X, y, cv=kf)
np.average(scores_lg)

"""### Evaluate Decision Tree"""

from sklearn.tree import DecisionTreeClassifier

scores_dt = cross_val_score(DecisionTreeClassifier(), X, y, cv=kf)
np.average(scores_dt)

### Evaluate Ramdom Forest Classifer

from sklearn.ensemble import RandomForestClassifier

scores_rf = cross_val_score(RandomForestClassifier(n_estimators=40), X, y, cv=kf)
np.average(scores_rf)

scores_rf = cross_val_score(RandomForestClassifier(n_estimators=40), X, y, cv=kf, scoring='roc_auc')
np.average(scores_rf)

from sklearn.model_selection import cross_validate

cross_validate(RandomForestClassifier(n_estimators=40), X, y, cv=kf, scoring=['accuracy', 'roc_auc'])
