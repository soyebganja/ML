# -*- coding: utf-8 -*-
"""11.5:Model_evaluation_Exercise1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TCZKc1eWAH5wnLe36VIldu3LT04fMb0p

### Problem Statement

You are a data scientist / AI engineer working on a classification problem to predict the likelihood of heart failure events based on clinical records. You have been provided with a dataset named **`"heart_failure_clinical_records.csv"`** which includes various clinical parameters of patients. The dataset comprises the following columns:

- age: Age of the patient (years)
- anaemia: Decrease of red blood cells or hemoglobin (boolean)
- creatinine_phosphokinase: Level of the CPK enzyme in the blood (mcg/L)
- diabetes: If the patient has diabetes (boolean)
- ejection_fraction: Percentage of blood leaving the heart at each contraction (percentage)
- high_blood_pressure: If the patient has hypertension (boolean)
- platelets: Platelets in the blood (kiloplatelets/mL)
- serum_creatinine: Level of serum creatinine in the blood (mg/dL)
- serum_sodium: Level of serum sodium in the blood (mEq/L)
- sex: Sex of the patient (binary, 1 for male, 0 for female)
- smoking: If the patient smokes or not (boolean)
- time: Follow-up period (days)
- death_event: If the patient died during the follow-up period (boolean)

Your task is to use this dataset to build and evaluate machine learning models to predict heart failure events. You will perform data preprocessing, exploratory data analysis, and model training using GaussianNB, SVM, and XGBoost. Additionally, you will use ROC curves to analyze model performance and make cost-benefit decisions.

**Dataset credits:** Heart Failure Clinical Records. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5Z89R.

**Import Necessary Libraries**
"""

# Import Necessary Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score, auc, roc_curve, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
import matplotlib.pyplot as plt

"""### Task 1: Data Preprocessing and Exploratory Data Analysis

1. Import the data from the `"heart_failure_clinical_records.csv"` file and store it in a DataFrame.
2. Display the number of rows and columns in the dataset.
3. Display the first few rows of the dataset to get an overview.
4. Check for missing values and handle them appropriately.
5. Perform basic statistical analysis and visualization to understand the distribution of each feature.
    - Use `histograms` for continuous features (age, creatinine_phosphokinase, ejection_fraction, platelets, serum_creatinine, serum_sodium, time).
    - Use `bar plots` for binary features (anaemia, diabetes, high_blood_pressure, sex, smoking).
"""

# Import the data from the "heart_failure_clinical_records.csv" file and store it in a DataFrame.
df = pd.read_csv('heart_failure_clinical_records.csv')


# Display the number of rows and columns in the dataset.
print(df.shape)


# Display the first few rows of the dataset to get an overview
df.head()

# Check for missing values and handle them appropriately.
df.isnull().sum()

# Perform basic statistical analysis and visualization to understand the distribution of each feature

#i) Histograms for continuous features (age, creatinine_phosphokinase, ejection_fraction, platelets, serum_creatinine, serum_sodium, time).
df[['age', 'creatinine_phosphokinase', 'ejection_fraction', 'platelets', 'serum_creatinine', 'serum_sodium', 'time']].hist(bins=20, color='skyblue', edgecolor='black', figsize=(15, 10))
plt.show()

# Bar plots for binary features (anaemia, diabetes, high_blood_pressure, sex, smoking).
binary_features = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']

for feature in binary_features:
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x=feature, hue='death_event', palette='Set2')
    plt.title(f'Death Event by {feature}')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.show()

"""### Task 2: Feature Transformation

1. Split the dataset into training and test sets with a test size of 25%.
2. Normalize continuous features (age, creatinine_phosphokinase, ejection_fraction, platelets, serum_creatinine, serum_sodium, time) using StandardScaler.
"""

# Split the dataset into training and test sets
X = df.drop('death_event', axis=1)
y = df['death_event']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Normalize continuous features using StandardScaler
standard_scaler = StandardScaler()

# Normalize continuous features (age, creatinine_phosphokinase, ejection_fraction, platelets, serum_creatinine, serum_sodium, time)
continuous_features = ['age', 'creatinine_phosphokinase', 'ejection_fraction', 'platelets', 'serum_creatinine', 'serum_sodium', 'time']
X_train[continuous_features] = standard_scaler.fit_transform(X_train[continuous_features])
X_test[continuous_features] = standard_scaler.transform(X_test[continuous_features])

"""### Task 3: Model Training and Evaluation with GaussianNB

1. Initialize and train a `GaussianNB` model using the training data.
2. Print the classification report to evaluate the model's performance.
3. Calculate the AUC for the GaussianNB model.
4. Find the probability threshold associated with a desired recall of 85% and print the corresponding false positive rate.
"""

# Initialize and train a GaussianNB model
GaussianNB_model = GaussianNB()
GaussianNB_model.fit(X_train, y_train)

# Print the classification report
y_pred = GaussianNB_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Calculate the AUC for the GaussianNB model.
probabilities_nb = GaussianNB_model.predict_proba(X_test)[:, 1]
fpr_nb, tpr_nb, thresholds_nb = roc_curve(y_test, probabilities_nb)
roc_auc_nb = auc(fpr_nb, tpr_nb)
print("AUC for GaussianNB:", roc_auc_nb)

# Find the probability threshold associated with 85% recall
desired_recall_nb = 0.85
cloest_index_nb = np.argmin(np.abs(tpr_nb - desired_recall_nb))
optimal_threshold_nb = thresholds_nb[cloest_index_nb]
optimal_fpr_nb = fpr_nb[cloest_index_nb]
print("Optimal Threshold for GaussianNB:", optimal_threshold_nb)
print("Optimal False Positive Rate for GaussianNB:", optimal_fpr_nb)

"""### Task 4: Model Training and Evaluation with SVM

1. Initialize and train an `SVM` model with a linear kernel using the training data.
2. Print the classification report to evaluate the model's performance.
3. Calculate the AUC for the SVM model.
4. Find the probability threshold associated with a desired recall of 90% and print the corresponding false positive rate.
"""

# Initialize and train an SVM model with a linear kernel
svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)


# Print the classification report
y_pred = svm_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Calculate the AUC
probabilities_svm = svm_model.predict_proba(X_test)[:, 1]
fpr_svm, tpr_svm, thresholds_svm = roc_curve(y_test, probabilities_svm)
roc_auc_svm = auc(fpr_svm, tpr_svm)
print("AUC for SVM:", roc_auc_svm)

# Find the probability threshold associated with 90% recall
desired_recall_svm = 0.90
cloest_index_svm = np.argmin(np.abs(tpr_svm - desired_recall_svm))
optimal_threshold_svm = thresholds_svm[cloest_index_svm]
optimal_fpr_svm = fpr_svm[cloest_index_svm]
print("Optimal Threshold for SVM:", optimal_threshold_svm)
print("Optimal False Positive Rate for SVM:", optimal_fpr_svm)

"""### Task 5: Model Training and Evaluation with XGBoost

1. Initialize and train an `XGBoost` model using the training data.
2. Print the classification report to evaluate the model's performance.
3. Calculate the AUC for the XGBoost model.
"""

# Initialize and train an XGBoost model
xgb_model = XGBClassifier()
xgb_model.fit(X_train, y_train)


# Print the classification report
y_pred = xgb_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Calculate the AUC
probabilities_xgb = xgb_model.predict_proba(X_test)[:, 1]
fpr_xgb, tpr_xgb, thresholds_xgb = roc_curve(y_test, probabilities_xgb)
roc_auc_xgb = auc(fpr_xgb, tpr_xgb)
print("AUC for XGBoost:", roc_auc_xgb)

"""### Task 6: Summary and Conclusion

1. Plot the ROC curves for `GaussianNB, SVM, and XGBoost` models on the same chart.
2. Summarize the results and compare the performance of the models.
"""

# Plot the ROC curves for all models
plt.figure(figsize=(8, 6))
plt.plot(fpr_nb, tpr_nb, label='GaussianNB (AUC = %0.2f)' % roc_auc_score(y_test, GaussianNB_model.predict_proba(X_test)[:, 1]))
plt.plot(fpr_svm, tpr_svm, label='SVM (AUC = %0.2f)' % roc_auc_score(y_test, svm_model.predict_proba(X_test)[:, 1]))
plt.plot(fpr_xgb, tpr_xgb, label='XGBoost (AUC = %0.2f)' % roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic(ROC) Curves')
plt.legend(loc="lower right")
plt.show()

"""### Conclusion

--------
--------
From the results, we can draw the following conclusions based on the performance metrics achieved by each model:

    GaussianNB Model:
        Accuracy: 0.80
        AUC: 0.88
        Provides a baseline performance with a recall of 47% for the positive class.

    SVM Model:
        Accuracy: 0.85
        AUC: 0.89
        Shows improvement over GaussianNB, achieving a recall of 76% for the positive class.

    XGBoost Model:
        Accuracy: 0.99
        AUC: 1.00
        Outperforms other models, providing superior performance and generalization.

In summary, while GaussianNB and SVM models provide reasonable performance, XGBoost models achieve higher accuracy and AUC, making them more suitable for this classification task. XGBoost, in particular, shows the best overall performance, making it the ideal choice for the heart failure prediction problem.

"""

