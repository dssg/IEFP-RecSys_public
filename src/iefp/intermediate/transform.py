import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import numpy as np
import yaml

from iefp.processing import CleanPedidos


class TransformToJourneys(luigi.Task):
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    s3path = buckets["intermediate"]["transform"]

    def requires(self):
        return CleanPedidos()

    def output(self):
        return S3Target(self.s3path + "journeys.parquet")

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = self.transform_journeys(df)
        df.to_parquet(self.output().path)

    def transform_journeys(self, df):
        df = df.sort_values(["ute_id", "data_movimento"], ascending=True)
        df["journey_start"] = df["tipo_movimento"] == 11
        df["journey_count"] = df.groupby("ute_id")["journey_start"].cumsum()

        # TODO: Do we need values from other movement codes
        # TODO: What about multiple registers (21) at the same day?
        # TODO: What about cases where multiple exits (31, 21) after each other?
        # TODO: What about cases where exit is successful vocational training?
        # In newer times these people just go to 'busy'
        df = df.loc[
            df["tipo_movimento"].isin([11, 21, 31]),
            [
                "ute_id",
                "journey_count",
                "data_movimento",
                "tipo_movimento",
                "motivo_inscricao",
                "motivo_anulacao",
            ],
        ]

        # NOTE: Convert to string for column join
        df["tipo_movimento"] = df["tipo_movimento"].astype("int").astype("str")
        df = df.pivot_table(
            index=["ute_id", "journey_count"], columns="tipo_movimento", aggfunc=np.min
        )
        df.columns = ["_".join(col).strip() for col in df.columns.values]
        df = df.reset_index()

        cols_port = [
            "ute_id",
            "journey_count",
            "data_movimento_11",
            "data_movimento_21",
            "data_movimento_31",
            "motivo_anulacao_31",
            "motivo_inscricao_11",
        ]
        cols_eng = [
            "user_id",
            "journey_count",
            "register_date",
            "exit_date_21",
            "exit_date_31",
            "exit_reason",
            "register_reason",
        ]
        df = df[cols_port]
        df.columns = cols_eng

        # Drop journeys where we don't have data about start or end
        df = df[df["journey_count"] > 0]
        df = df[(df["exit_date_21"].notna()) | (df["exit_date_31"].notna())]
        return df
