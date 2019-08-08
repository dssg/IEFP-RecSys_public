import luigi
import pandas as pd
import yaml

from datetime import datetime
from luigi.contrib.s3 import S3Target
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from iefp.data import write_object_to_s3
from iefp.modelling import SplitTrainTest


class TrainRandomForest(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())

    def requires(self):
        return SplitTrainTest(self.date)

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        target_path = buckets["models"]

        return S3Target(
            target_path
            + "{date:%Y/%m/%d/random_forest_T%H%M%S.pkl}".format(date=self.date)
        )

    def run(self):
        df_train = pd.read_parquet(self.input()[0].path)
        y_train = df_train.loc[:, "ttj_sub_12"]
        X_train = df_train.drop(["ttj", "ttj_sub_12"], axis="columns")

        grid = yaml.load(open("./conf/base/parameters.yml"), Loader=yaml.FullLoader)[
            "rf_small_grid"
        ]
        model = self.train_rf_cv(X_train, y_train, scoring_metric="f1", grid=grid)

        write_object_to_s3(model, self.output().path)

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
