import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import yaml

from iefp.processing import CleanPedidos


class AddDemographics(luigi.Task):
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    target_path = buckets["intermediate"]["transform"]
    clean_path = buckets["intermediate"]["clean"]

    def requires(self):
        return TransformToJourneys()

    def output(self):
        return S3Target(self.target_path + "dem_journeys.parquet")

    def run(self):
        df_pedidos = pd.read_parquet(self.clean_path + "pedidos.parquet")
        df_journeys = pd.read_parquet(self.input().path)
        df_journeys = self.add_demographics(df_pedidos, df_journeys)
        df_journeys.to_parquet(self.output().path)

    def add_demographics(self, df_pedidos, df_journey):
        dem_cols = yaml.load(
            open("./conf/base/column_dict.yml"), Loader=yaml.FullLoader
        )

        df_pedidos = df_pedidos[df_pedidos["tipo_movimento"] == 11]
        df_pedidos = df_pedidos.sort_values(
            ["ute_id", "data_movimento"], ascending=True
        )
        df_pedidos = df_pedidos.groupby(["ute_id", "data_movimento"]).first()
        df_pedidos = df_pedidos.drop_duplicates()

        # Filter and rename columns
        df_pedidos = df_pedidos[dem_cols.keys()]
        df_pedidos = df_pedidos.rename(dem_cols, axis="columns")

        df_journey = df_journey.merge(
            df_pedidos,
            left_on=["user_id", "register_date"],
            right_on=["ute_id", "data_movimento"],
            how="left",
        )

        return df_journey


class TransformToJourneys(luigi.Task):
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    target_path = buckets["intermediate"]["transform"]

    def requires(self):
        return CleanPedidos()

    def output(self):
        return S3Target(self.target_path + "raw_journeys.parquet")

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = self.transform_journeys(df)
        df.to_parquet(self.output().path)

    def transform_journeys(self, df):
        df = df.sort_values(["ute_id", "data_movimento"], ascending=True)
        df["journey_start"] = df["tipo_movimento"] == 11
        df["journey_count"] = df.groupby("ute_id")["journey_start"].cumsum()

        df = df.loc[
            df["tipo_movimento"].isin([11, 21, 31]),
            [
                "ute_id",
                "journey_count",
                "data_movimento",
                "tipo_movimento",
                "motivo_inscricao",
                "motivo_anulacao",
                "estado",
            ],
        ]

        # NOTE: Convert to string for column join
        df["tipo_movimento"] = df["tipo_movimento"].astype("int").astype("str")

        # Assumption: Use first exit if multiple.
        df = df.pivot_table(
            index=["ute_id", "journey_count"], columns="tipo_movimento", aggfunc="first"
        )

        df.columns = ["_".join(col).strip() for col in df.columns.values]
        df = df.reset_index()

        cols_port = [
            "ute_id",
            "journey_count",
            "data_movimento_11",
            "motivo_inscricao_11",
            "estado_11",
            "data_movimento_21",
            "data_movimento_31",
            "motivo_anulacao_31",
        ]
        cols_eng = [
            "user_id",
            "journey_count",
            "register_date",
            "register_reason",
            "register_status",
            "exit_date_21",
            "exit_date_31",
            "exit_reason",
        ]
        df = df[cols_port]
        df.columns = cols_eng

        # Drop journeys where we don't have data about start or end
        df = df[
            (df["register_date"].notna())
            & ((df["exit_date_21"].notna()) | (df["exit_date_31"].notna()))
        ]
        # Drop journeys of people that are not activly searching for emplpoyment
        df = df[df["register_status"] == "ACT"]
        return df
