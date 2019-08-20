import luigi

from datetime import datetime
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from iefp.data import model_info_to_db
from iefp.data import get_db_engine
from iefp.data import s3
from iefp.modelling import SplitTrainTest
from iefp.modelling import (
    TrainRandomForest,
    TrainLogisticRegression,
    TrainGradientBoosting,
)


class EvaluateGradientBoosting(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())
    task_complete = False

    def requires(self):
        return [SplitTrainTest(), TrainGradientBoosting(self.date)]

    def run(self):
        df_test = s3.read_parquet(self.input()[0][1].path)
        y_test = df_test.loc[:, "ttj_sub_12"]
        X_test = df_test.drop(["ttj", "ttj_sub_12"], axis="columns")

        gb = s3.read_pickle(self.input()[1].path)
        metrics = evaluate(gb, X_test, y_test)

        model_info_to_db(
            engine=get_db_engine(),
            model=gb,
            metrics=metrics,
            features=X_test.columns.tolist(),
            date=self.date,
            model_path=self.input()[1].path,
            train_data_path=self.input()[0][2].path,
            test_data_path=self.input()[0][3].path,
        )
        # NOTE: Set task as completed manually. Use the build-in
        # luigi.contrib.postgres.CopyToTable Task would the right.
        self.task_complete = True

    def complete(self):
        return self.task_complete


class EvaluateRandomForest(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())
    task_complete = False

    def requires(self):
        return [SplitTrainTest(), TrainRandomForest(self.date)]

    def run(self):
        df_test = s3.read_parquet(self.input()[0][1].path)
        y_test = df_test.loc[:, "ttj_sub_12"]
        X_test = df_test.drop(["ttj", "ttj_sub_12"], axis="columns")

        rf = s3.read_pickle(self.input()[1].path)
        metrics = evaluate(rf, X_test, y_test)

        model_info_to_db(
            engine=get_db_engine(),
            model=rf,
            metrics=metrics,
            features=X_test.columns.tolist(),
            date=self.date,
            model_path=self.input()[1].path,
            train_data_path=self.input()[0][2].path,
            test_data_path=self.input()[0][3].path,
        )
        # NOTE: Set task as completed manually. Use the build-in
        # luigi.contrib.postgres.CopyToTable Task would the right.
        self.task_complete = True

    def complete(self):
        return self.task_complete


class EvaluateLogisticRegression(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())
    task_complete = False

    def requires(self):
        return [SplitTrainTest(), TrainLogisticRegression(self.date)]

    def run(self):
        df_test = s3.read_parquet(self.input()[0][1].path)
        y_test = df_test.loc[:, "ttj_sub_12"]
        X_test = df_test.drop(["ttj", "ttj_sub_12"], axis="columns")

        lg = s3.read_pickle(self.input()[1].path)
        metrics = evaluate(lg, X_test, y_test)

        model_info_to_db(
            engine=get_db_engine(),
            model=lg,
            metrics=metrics,
            features=X_test.columns.tolist(),
            date=self.date,
            model_path=self.input()[1].path,
            train_data_path=self.input()[0][2].path,
            test_data_path=self.input()[0][3].path,
        )
        # NOTE: Set task as completed manually. Use the build-in
        # luigi.contrib.postgres.CopyToTable Task would the right.
        self.task_complete = True

    def complete(self):
        return self.task_complete


def evaluate(clf, X, y):
    """
    Evaluates accuracy, f1, precision and recall of classifier

    :param X: Feature matrix of test set
    :param y: Target vector of test set
    :return dict: accuracy, f1, precision, recall
    """
    y_pred = clf.predict(X)

    accuracy = round(accuracy_score(y, y_pred), 4)
    f1 = round(f1_score(y, y_pred), 4)
    precision = round(precision_score(y, y_pred), 4)
    recall = round(recall_score(y, y_pred), 4)

    metrics = {
        "m_accuracy": accuracy,
        "m_f1": f1,
        "m_precision": precision,
        "m_recall": recall,
    }
    return metrics
