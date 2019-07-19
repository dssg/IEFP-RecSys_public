import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import yaml

from iefp.data.constants import Movement, Status
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
            open("./conf/base/demographic_translation.yml"), Loader=yaml.FullLoader
        )

        df_pedidos = df_pedidos[df_pedidos["tipo_movimento"] == Movement.REGISTRATION]
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
        df["journey_start"] = df["tipo_movimento"] == Movement.REGISTRATION
        df["journey_count"] = df.groupby("ute_id")["journey_start"].cumsum()

        journey_codes = [
            Movement.REGISTRATION,
            Movement.JOB_PLACEMENT_IEFP,
            Movement.CANCELLATION,
        ]
        df = df.loc[
            df["tipo_movimento"].isin(journey_codes),
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
        # Consequence: If start and end at the same day, even though
        # there were later exit dates, these journeys will be filtered out.
        df = df.pivot_table(
            index=["ute_id", "journey_count"], columns="tipo_movimento", aggfunc="first"
        )

        df.columns = ["_".join(col).strip() for col in df.columns.values]
        df = df.reset_index()

        #
        # Translate columns
        #
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

        #
        # Filter
        #

        # Drop journeys where we don't have data about start or end
        df = df[
            (df["register_date"].notna())
            & ((df["exit_date_21"].notna()) | (df["exit_date_31"].notna()))
        ]
        # Drop journeys of people that are not activly searching for emplpoyment
        df = df[df["register_status"] == Status.ACTIVE]
        df = df.drop(["register_status"], axis="columns")

        # If person has an exit at the same date of registration or
        # another exit later, set the same-day exit to NaT
        df.loc[
            (df.register_date == df.exit_date_21) & df.exit_date_31.notna(),
            "exit_date_21",
        ] = pd.NaT
        df.loc[
            (df.register_date == df.exit_date_31) & df.exit_date_21.notna(),
            "exit_date_31",
        ] = pd.NaT

        # Drop journeys that start and end at the same day
        df["one_day_journey"] = (df.register_date == df.exit_date_21) | (
            df.exit_date_31 == df.register_date
        )
        df = df[df["one_day_journey"] == False]
        df = df.drop(["one_day_journey"], axis="columns")

        return df
