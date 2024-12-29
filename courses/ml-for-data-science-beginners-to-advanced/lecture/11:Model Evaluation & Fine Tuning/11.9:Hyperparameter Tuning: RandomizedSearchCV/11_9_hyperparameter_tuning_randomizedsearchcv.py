# -*- coding: utf-8 -*-
"""11.9:Hyperparameter Tuning: RandomizedSearchCV.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19Lj9pIdNK-HHzp78qi0xaIQLEmT6FiEK
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=8,
    n_redundant=2,
    n_repeated=0,
    n_classes=2,
    random_state=42
)

"""### GridSearchCV"""

grid_search = GridSearchCV(
    DecisionTreeClassifier(),
    {
        'criterion': ['gini', 'entropy'],
        'max_depth': [5, 10, 15, 20],
    },
    cv=5,
    return_train_score=False
)
grid_search.fit(X, y)
df = pd.DataFrame(grid_search.cv_results_).sort_values('rank_test_score')
df[["param_criterion", "param_max_depth", "mean_test_score"]]

grid_search = RandomizedSearchCV(
    DecisionTreeClassifier(),
    {
        'criterion': ['gini', 'entropy'],
        'max_depth': [5, 10, 15, 20],
    },
    cv=5,
    return_train_score=False,
    n_iter=3
)
grid_search.fit(X, y)
df = pd.DataFrame(grid_search.cv_results_).sort_values('rank_test_score')
df[["param_criterion", "param_max_depth", "mean_test_score"]]

