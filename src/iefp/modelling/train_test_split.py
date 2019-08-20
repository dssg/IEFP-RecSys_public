import luigi
import numpy as np

from datetime import datetime
from luigi.contrib.s3 import S3Target
from sklearn.preprocessing import MinMaxScaler

from iefp.data import s3
from iefp.data.constants import S3
from iefp.modelling import CreateModellingTable


class SplitTrainTest(luigi.Task):
    date = luigi.DateSecondParameter(default=datetime.now())

    def requires(self):
        return CreateModellingTable()

    def output(self):
        return [
            S3Target(s3.path(S3.MODELLING + "train.parquet")),
            S3Target(s3.path(S3.MODELLING + "test.parquet")),
            S3Target(
                s3.path(
                    S3.MODELS
                    + "{date:%Y/%m/%d/train_T%H%M%S.parquet}".format(date=self.date)
                )
            ),
            S3Target(
                s3.path(
                    S3.MODELS
                    + "{date:%Y/%m/%d/test_T%H%M%S.parquet}".format(date=self.date)
                )
            ),
        ]

    def run(self):
        df_modelling = s3.read_parquet(self.input().path)
        df_train, df_test = self.train_test_split(df_modelling)
        df_train, df_test = self.scale_numeric_feats(df_train, df_test)

        # NOTE: Save both datasets twice.
        # - One set that is tied to a trained model
        # - One set that gets overwritten with the current one
        s3.write_parquet(df_train, self.output()[0].path)
        s3.write_parquet(df_test, self.output()[1].path)
        s3.write_parquet(df_train, self.output()[2].path)
        s3.write_parquet(df_test, self.output()[3].path)

    def train_test_split(self, df_modelling):
        """
        Split modelling table into training and test set.
        Keep most recent-year long data as test set.

        :param df_train: Training dataframe
        :param df_test: Test dataframe
        :return: tuple(df_train, df_test)
        """

        cutoff = df_modelling["exit_date"].max() - np.timedelta64(1, "Y")

        df_train = df_modelling[df_modelling["exit_date"] < cutoff].drop(
            "exit_date", axis="columns"
        )
        df_test = df_modelling[df_modelling["exit_date"] >= cutoff].drop(
            "exit_date", axis="columns"
        )

        # Resample into training set to to 80/20 ratio if test set is larger
        test_size = round((len(df_train) + len(df_test)) * 0.2)
        if len(df_test) > test_size:
            df_sample = df_test.sample(n=(len(df_test) - test_size), random_state=1)
            df_test = df_test.drop(df_sample.index)
            df_train = df_train.append(df_sample)

        return df_train, df_test

    def scale_numeric_feats(self, df_train, df_test):
        """
        Scales numeric feats of test and training set.
        Scale test set with training scaler, to prevent data leakage

        :param df_train: Training dataframe
        :param df_test: Test dataframe
        :return: tuple(df_train, df_test)
        """
        scaler = MinMaxScaler()

        num_cols = list(df_train.select_dtypes(include=[np.number]))
        scaler.fit(df_train[num_cols])

        df_train[num_cols] = scaler.transform(df_train[num_cols])
        df_test[num_cols] = scaler.transform(df_test[num_cols])
        return df_train, df_test
