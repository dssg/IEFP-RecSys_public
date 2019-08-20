import luigi
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import Category, Movement, RegistrationReason, S3, Status
from iefp.processing import CleanPedidos


class TransformToJourneys(luigi.Task):
    def requires(self):
        return CleanPedidos()

    def output(self):
        return S3Target(s3.path(S3.TRANSFORM + "raw_journeys.parquet"))

    def run(self):
        df = s3.read_parquet(self.input().path)
        df = self.transform_journeys(df)
        s3.write_parquet(df, self.output().path)

    def transform_journeys(self, df):
        """
        Function transforms Pedidos dataframe to a journeys table,
        where each row represents a journey from unemployment to employment
        of a particular user. Users can have multiple journeys.

        Journeys are generated as follows:

        1. Define start of the journey as:
            a) Movement 11 with Category: Unemployed (1,2)
            b) Movement 43 with Category: Unemployed (1,2) or
            Employed (3,4) but register reason: Not paid (17)

        2. Define end of the journey as:
            a) Movement 31 or 21
            b) Movement 43 with Category: Employed (3,4)

        3. Group by journey-ends and their journey count
            Use first occuring start (if multiple ) as the start of the journey

        :param df: Cleaned and extracted pedidos pd.dataframe
        :return: Skeleton journeys dataframe
        """

        df = df.sort_values(["ute_id", "data_movimento"], ascending=True)

        unemployed_codes = [Category.UNEMPLOYED_FIRST_JOB, Category.UNEMPLOYED_NEW_JOB]
        employed_codes = [Category.EMPLOYED, Category.EMPLOYED_PART_TIME]
        df["start_journey"] = (
            (
                (df.tipo_movimento == Movement.REGISTRATION)
                & df.categoria.isin(unemployed_codes)
            )
            | (
                (df.tipo_movimento == Movement.REGISTRATION)
                & (df.motivo_inscricao == RegistrationReason.NOT_PAID)
            )
            | (
                (df.tipo_movimento == Movement.CATEGORY_CHANGE)
                & df.categoria.isin(unemployed_codes)
            )
            | (
                (df.tipo_movimento == Movement.CATEGORY_CHANGE)
                & (df.motivo_inscricao == RegistrationReason.NOT_PAID)
            )
        )
        df["end_journey"] = (
            (df.tipo_movimento == Movement.JOB_PLACEMENT_IEFP)
            | (df.tipo_movimento == Movement.CANCELLATION)
            | (
                (df.tipo_movimento == Movement.CATEGORY_CHANGE)
                & df.categoria.isin(employed_codes)
            )
        )

        # Determine journeys by their end (which is not ambigious)
        # NOTE: Subtract 1 where journey ends, so it belongs to the previous journey
        df["journey_count"] = (
            df.groupby("ute_id")["end_journey"].cumsum() - df["end_journey"]
        )

        # Put start and end into one column so we can better pivot on it
        df.loc[df.start_journey == True, "journey"] = "start"
        df.loc[df.end_journey == True, "journey"] = "end"
        df = df.drop(["start_journey", "end_journey"], axis="columns")
        df = df.pivot_table(
            index=["ute_id", "journey_count"], columns="journey", aggfunc="first"
        )

        # Format column names for better renaming
        df.columns = ["_".join(col).strip() for col in df.columns.values]
        df = df.reset_index()

        df = df[
            [
                "ute_id",
                "journey_count",
                "data_movimento_start",
                "data_movimento_end",
                "tipo_movimento_start",
                "tipo_movimento_end",
                "estado_start",
                "categoria_start",
                "categoria_end",
                "motivo_inscricao_start",
                "motivo_anulacao_end",
            ]
        ]
        df.columns = [
            "user_id",
            "journey_count",
            "register_date",
            "exit_date",
            "register_movement",
            "exit_movement",
            "register_status",
            "register_category",
            "exit_category",
            "register_reason",
            "exit_reason",
        ]

        return df


class FilterJourneys(luigi.Task):
    def requires(self):
        return TransformToJourneys()

    def output(self):
        return S3Target(s3.path(S3.TRANSFORM + "filtered_journeys.parquet"))

    def run(self):
        df = s3.read_parquet(self.input().path)
        df = self.filter_journeys(df)
        s3.write_parquet(df, self.output().path)

    def filter_journeys(self, df):
        """
        Function filters out incomplete and invalid journeys from the journeys table

        :param df: Skeleton journeys pd.dataframe
        :return: Returns filered journeys dataframe
        """

        # Drop journeys of people that are not activly searching for emplpoyment
        df = df[df["register_status"] == Status.ACTIVE]
        df = df.drop(["register_status"], axis="columns")

        # Drop journeys where we don't have data about start or end
        # I.e. incomplete journeys at the beginning or end of the data
        df = df[(df["register_date"].notna()) & (df["exit_date"].notna())]

        # Drop journeys that start and end at the same day
        df = df[df["register_date"].dt.date != df["exit_date"].dt.date]
        return df


class AddDemographics(luigi.Task):
    def requires(self):
        return [CleanPedidos(), FilterJourneys()]

    def output(self):
        return S3Target(s3.path(S3.TRANSFORM + "filtered_journeys.parquet"))

    def run(self):
        df_pedidos = s3.read_parquet(self.input()[0].path)
        df_journeys = s3.read_parquet(self.input()[1].path)
        df_journeys = self.add_demographics(df_pedidos, df_journeys)
        s3.write_parquet(df_journeys, self.output().path)

    def add_demographics(self, df_pedidos, df_journey):
        """
        Function adds demographic information to journeys table.
        Demographics are taken from the pedidos table at the time of the journey start

        :param df: Filtered journeys pd.dataframe
        :return: Returns journeys dataframe with demographic information
        """
        dem_cols = yaml.load(
            open("./conf/base/demographic_translation.yml"), Loader=yaml.FullLoader
        )

        df_pedidos = df_pedidos[
            df_pedidos["tipo_movimento"].isin(
                [Movement.REGISTRATION, Movement.CATEGORY_CHANGE]
            )
        ]
        df_pedidos = df_pedidos.sort_values(
            ["ute_id", "data_movimento"], ascending=True
        )
        df_pedidos = df_pedidos.groupby(["ute_id", "data_movimento"]).last()

        df_pedidos = df_pedidos[dem_cols.keys()]
        df_pedidos = df_pedidos.rename(dem_cols, axis="columns")

        df_pedidos = df_pedidos.reset_index()
        df_journey = df_journey.merge(
            df_pedidos,
            left_on=["user_id", "register_date"],
            right_on=["ute_id", "data_movimento"],
            how="left",
        )

        return df_journey
