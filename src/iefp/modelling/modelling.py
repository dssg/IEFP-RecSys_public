import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import pickle

from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import auc, roc_curve
from sklearn.metrics import f1_score

from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier


from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from scipy.stats import randint

import itertools

# evaluation

def evaluate(y_test, y_pred, y_prob):
    results = "\n---"
    results = results + str(confusion_matrix(y_test, y_pred)) + "\n---" + "Accuracy: {:.2f}%".format(100 * accuracy_score(y_test, y_pred)) + "\n---"
        
    results = results + str(average_precision_score(y_test, y_pred))
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    results = results + "{:.2f}% Precision at {}% Recall".format(100 * precision[recall>0.8].max(), 80) + "\n"
    results = results + "Precision: " + str(precision) + "\n" + "Recall: " + str(recall)
    return results


print("running...")

df = pd.read_parquet("s3://iefp-unemployment/modelling/modelling.parquet")


# modelling table construction

def transform_interventions(df: pd.DataFrame, interventions: list):
    df = df[interventions]
    df = (df.notna()).astype('int')
    
    return df


def construct_table(df): 
    # Filter for frequent interventions
    # WARNING: data leakage
    # frequent_i = df_model.mean()[df_model.mean() > 0.01].index.tolist()
    # df_model = df_model[frequent_i]
    
    
    interv_cols = [col for col in df.columns if "i_" in col]
    df_model = transform_interventions(df, interv_cols)
    
    dems = [
    "d_age",
    "d_gender",
    "d_civil_status",
    "d_rsi",
    "d_desired_work_time",
    "d_desired_contract",
    "d_disabled",
    "d_nationality",
    "d_desired_job_sector",
    "d_previous_job_sector",
    "d_school_qualification", 
    "d_college_qualification",
    "d_subsidy",
    "d_previous_job_experience",
    "register_reason",
    "d_parish",
    "d_professional_training"
    ]
    
    df_model[dems] = df[dems]
    
    # Dealing with missing values
    # Leave None type as feature in college_qual
    # Fill NAs with 0 for school qualification!!!
    # Fill NAs with 0 for previous job experience

    df_model['d_school_qualification'] = df_model['d_school_qualification'].fillna(0)
    df_model['d_previous_job_experience'] = df_model['d_previous_job_experience'].fillna(0)

    # Seasonal features
    # Encode temporal variables as strings to enable dummy var creation
    df_model["register_month"] = df.register_date.dt.month.astype(str)
    df_model["register_year"] = df.register_date.dt.year.astype(str)

    
    df_model = pd.get_dummies(df_model, drop_first=True, dummy_na=True)

    # Output
    df_model["ttj_sub_12"] = (df["journey_length"] < 365) & (df["success"] == True)
    
    return df_model

def run_grid_pipe(data, pipeline, gs_params, filename):
    
    # Get holdout set

    data["exit_date"] = df["exit_date"]
    df_hold_out = data[data["exit_date"] >= "2019-01-01"].drop("exit_date", axis=1)

    # Get training set

    data["exit_date"] = df["exit_date"]
    df_train = data[data["exit_date"] <= "2019-01-01"].drop("exit_date", axis=1)

    y = df_train["ttj_sub_12"]
    X = df_train.drop("ttj_sub_12", axis=1)
    
    grid_search = GridSearchCV(pipeline, gs_params, cv=5, refit=True, scoring="average_precision")

    grid_search.fit(X, y)

    final_model = grid_search.best_estimator_

    y_pred = final_model.predict(X)
    y_prob = final_model.predict_proba(X)[:,1]

    training_evaluation = evaluate(y, y_pred, y_prob)

    # Train on all data and then test on holdout set

    final_model.fit(X, y)

    y_hold = df_hold_out["ttj_sub_12"]
    X_hold = df_hold_out.drop("ttj_sub_12", axis=1)

    y_test_pred = final_model.predict(X_hold)
    y_test_prob = final_model.predict_proba(X_hold)[:,1]

    test_evaluation = evaluate(y_hold, y_test_pred, y_test_prob)
    

    f = open("results.txt", "a")
    f.write("\n" + filename + "\n" + str(final_model) + "\n")
    f.write("Evaluation of model on training data: \n")
    f.write(training_evaluation)
    f.write("Evaluation of model on test data: \n")
    f.write(test_evaluation)
    f.write(str(confusion_matrix(y_hold, final_model.predict(X_hold))) + "\n")
    f.write(str(accuracy_score(y_hold, final_model.predict(X_hold))) + "\n")
    f.write("\n")
    f.close()

    # save the model to disk

    pickle.dump(final_model, open(filename, 'wb'))


##############################################

df_model = construct_table(df)

##############################################


# Prepare Random Forest pipeline with scaling (for Age and job experience)

rf__scale_pipeline = Pipeline([
    ('scale', MinMaxScaler()),
    ('rf', RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=0, class_weight="balanced"))
])


# RF Grid search

big_param_grid = [
        {'rf__n_estimators': [1,10,100,500,1000,2500],
         'rf__max_depth': [3,5,10,20,50,100],
         'rf__max_features': ['sqrt','log2'],
         'rf__min_samples_split': [2,5,10,20],
         'rf__n_jobs': [-1]
        },
    ]

med_param_grid = [
        {'rf__n_estimators': [1,10,100,1000],
         'rf__max_depth': [1,5,10,20],
         'rf__max_features': ['sqrt','log2'],
         'rf__min_samples_split': [2,5,10],
         'rf__n_jobs': [-1]
        },
    ]

param_grid = [
        {'rf__n_estimators': [500],
         'rf__max_depth': [2, 3]
        },
    ]

# Prepare LogReg pipeline

logreg_pipeline = Pipeline([
    ('scale', MinMaxScaler()),
    ('logreg', LogisticRegression(penalty='l1', C=1e5)),
])

# LR Grid search

lg_param_grid = [
        {'logreg__penalty': ['l1','l2'],
         'logreg__C': [0.00001,0.0001,0.001, 0.01,0.1,1,10]
        },
    ]

# Prepare Gradient boost pipeline

gboost_pipeline = Pipeline([
    ('scale', MinMaxScaler()),
    ('gboost', GradientBoostingClassifier(learning_rate=0.05, subsample=0.5, max_depth=6, n_estimators=10)),
])


# Gradient Boosting Trees Grid search

gb_param_grid = [
        {'gboost__n_estimators': [1,10,100,1000,10000],
         'gboost__learning_rate' : [0.001,0.01,0.05,0.1,0.5],
         'gboost__subsample' : [0.1,0.5,1.0],
         'gboost__max_depth': [1,3,5,10,20,50,100]
        },
    ]

# Prepare adaboost pipeline

adaboost_pipeline = Pipeline([
    ('scale', MinMaxScaler()),
    ('adaboost', AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME", n_estimators=200))
])


# Ada grid search

ada_param_grid = [
        {'algorithm': ['SAMME', 'SAMME.R'],
         'n_estimators': [1,10,100,500,1000,10000]
        },
    ]

# Prepare SVM pipeline

svm_pipeline = Pipeline([
    ('scale', MinMaxScaler()),
    ('svm', svm.SVC(kernel='linear', probability=True, random_state=0))
])

svm_param_grid = [
        {'C' :[0.00001,0.0001,0.001,0.01,0.1,1,10],
         'gamma':[1,0.1,0.001,0.0001],
         'kernel':['linear', 'rbf', 'polynomial', 'sigmoid']
        },
    ]

# Run pipelines

run_grid_pipe(df_model, rf__scale_pipeline, param_grid, "rf_test.sav")
run_grid_pipe(df_model, logreg_pipeline, lg_param_grid, "lg_test.sav")
run_grid_pipe(df_model, gboost_pipeline, gb_param_grid, "gb_test.sav")
run_grid_pipe(df_model, adaboost_pipeline, ada_param_grid, "ada_test.sav")
run_grid_pipe(df_model, svm_pipeline, svm_param_grid, "svm_test.sav")



print("Done!")
