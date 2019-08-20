import luigi
import yaml

from datetime import datetime
from luigi.contrib.s3 import S3Target
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

from iefp.data import s3
from iefp.data.constants import S3
from iefp.modelling import SplitTrainTest


class TrainGradientBoosting(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())

    def requires(self):
        return SplitTrainTest(self.date)

    def output(self):
        return S3Target(
            s3.path(
                S3.MODELS
                + "{date:%Y/%m/%d/gradient_boosting_T%H%M%S.pkl}".format(date=self.date)
            )
        )

    def run(self):
        df_train = s3.read_parquet(self.input()[0].path)
        y_train = df_train.loc[:, "ttj_sub_12"]
        X_train = df_train.drop(["ttj", "ttj_sub_12"], axis="columns")

        grid = yaml.load(open("./conf/base/parameters.yml"), Loader=yaml.FullLoader)[
            "rf_small_grid"
        ]
        model = self.train_gb_cv(X_train, y_train, scoring_metric="f1", grid=grid)

        s3.write_pickle(model, self.output().path)

    def train_gb_cv(self, X, y, scoring_metric, grid=dict()):
        """
        Runs grid search on a random forest classifier

        :param X: Feature matrix of training set
        :param y: Target vector of training set
        :param scoring_metric: Single metric from which we choose the best classifier
        :param grid: Cross validation grid
        :return: Best trained model after grid search
        """
        gb = GradientBoostingClassifier(random_state=0)
        gb_grid_search = GridSearchCV(
            gb, grid, scoring=scoring_metric, cv=5, refit=True
        )
        gb_grid_search.fit(X, y)

        return gb_grid_search.best_estimator_


class TrainRandomForest(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())

    def requires(self):
        return SplitTrainTest(self.date)

    def output(self):
        return S3Target(
            s3.path(
                S3.MODELS
                + "{date:%Y/%m/%d/random_forest_T%H%M%S.pkl}".format(date=self.date)
            )
        )

    def run(self):
        df_train = s3.read_parquet(self.input()[0].path)
        y_train = df_train.loc[:, "ttj_sub_12"]
        X_train = df_train.drop(["ttj", "ttj_sub_12"], axis="columns")

        grid = yaml.load(open("./conf/base/parameters.yml"), Loader=yaml.FullLoader)[
            "rf_small_grid"
        ]
        model = self.train_rf_cv(X_train, y_train, scoring_metric="f1", grid=grid)

        s3.write_pickle(model, self.output().path)

    def train_rf_cv(self, X, y, scoring_metric, grid=dict()):
        """
        Runs grid search on a random forest classifier

        :param X: Feature matrix of training set
        :param y: Target vector of training set
        :param scoring_metric: Single metric from which we choose the best classifier
        :param grid: Cross validation grid
        :return: Best trained model after grid search
        """
        rf = RandomForestClassifier(random_state=0, n_jobs=-1, class_weight="balanced")
        rf_grid_search = GridSearchCV(
            rf, grid, scoring=scoring_metric, cv=5, refit=True
        )
        rf_grid_search.fit(X, y)

        return rf_grid_search.best_estimator_


class TrainLogisticRegression(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())

    def requires(self):
        return SplitTrainTest(self.date)

    def output(self):
        return S3Target(
            s3.path(
                S3.MODELS
                + "{date:%Y/%m/%d/logistic_regression_T%H%M%S.pkl}".format(
                    date=self.date
                )
            )
        )

    def run(self):
        df_train = s3.read_parquet(self.input()[0].path)
        y_train = df_train.loc[:, "ttj_sub_12"]
        X_train = df_train.drop(["ttj", "ttj_sub_12"], axis="columns")

        grid = yaml.load(open("./conf/base/parameters.yml"), Loader=yaml.FullLoader)[
            "lg_small_grid"
        ]
        model = self.train_rf_cv(X_train, y_train, scoring_metric="f1", grid=grid)

        s3.write_pickle(model, self.output().path)

    def train_rf_cv(self, X, y, scoring_metric, grid=dict()):
        """
        Runs grid search on logistic regression

        :param X: Feature matrix of training set
        :param y: Target vector of training set
        :param scoring_metric: Single metric from which we choose the best classifier
        :param grid: Cross validation grid
        :return: Best trained model after grid search
        """
        lg = LogisticRegression(random_state=0, solver="liblinear")
        lg_grid_search = GridSearchCV(
            lg, grid, scoring=scoring_metric, cv=5, refit=True
        )
        lg_grid_search.fit(X, y)

        return lg_grid_search.best_estimator_
