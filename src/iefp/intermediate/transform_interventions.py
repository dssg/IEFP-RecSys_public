import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import numpy as np
import yaml

from iefp.intermediate import AddDemographics
from iefp.processing import CleanInterventions


class TransformInterventions(luigi.Task):
    def requires(self):
        return [CleanInterventions(), AddDemographics()]

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        s3path = buckets["intermediate"]["transform"]

        return S3Target(s3path + "intermediate.parquet")

    def run(self):
        df_interventions = pd.read_parquet(self.input()[0].path)
        df_journeys = pd.read_parquet(self.input()[1].path)
        df_journeys = self.transform_interventions(df_interventions, df_journeys)
        df_journeys.to_parquet(self.output().path)

    def transform_interventions(self, df_interventions, df_journeys):
        """
        Function adds interventions which occur within a jouney to the journey pd.dataframe

        - param df_interventions: Cleaned and extracted interventions pd.dataframe
        - param df_journeys: Most recent journey pd.dataframe with outcomes (one line per jouney)
        - return: Returns the intermediate layer as a wide pd.dataframe with journey
        information, demographics, and outcomes and one date column for each
        intervention code.
        """
        success = yaml.load(open("./conf/base/successful_intervention_results.yml"))
        recommendable_interventions = yaml.load(
            open("./conf/base/recommendable_interventions.yml")
        )

        # Filter interventions
        df_interventions = df_interventions[
            df_interventions.resultado_intervencao.isin(success)
        ]
        df_interventions = df_interventions[
            df_interventions.codigo_intervencao.isin(recommendable_interventions)
        ]
        df_interventions = df_interventions[
            ["ute_id", "data_intervencao", "codigo_intervencao"]
        ]
        df_interventions.codigo_intervencao = df_interventions.codigo_intervencao.astype(
            "str"
        )

        # Set index's and merge with basic journey info
        df_interventions = df_interventions.set_index("ute_id")
        df_journeys = df_journeys.set_index("user_id")
        df_output = df_journeys[["journey_count", "register_date", "exit_date"]].merge(
            df_interventions, how="inner", left_index=True, right_index=True
        )

        # Filter for interventions that occur between journey dates
        df_output = df_output[
            (df_output.data_intervencao >= df_output.register_date)
            & (df_output.data_intervencao <= df_output.exit_date)
        ]
        df_output = df_output[
            ["journey_count", "data_intervencao", "codigo_intervencao"]
        ]
        df_output.columns = ["journey_count", "intervention_date", "intervention_code"]

        # Pivot table
        df_output = df_output.reset_index().rename(columns={"index": "user_id"})
        df_output = df_output = df_output.set_index(["user_id", "journey_count"])
        df_output = df_output.pivot_table(
            index=["user_id", "journey_count"],
            columns=["intervention_code"],
            aggfunc=np.min,
        )
        df_output.columns = ["_".join(col).strip() for col in df_output.columns.values]

        # Merge pivot table with full journey table
        df_journeys = df_journeys.reset_index().rename(columns={"index": "user_id"})
        df_journeys = df_journeys.set_index(["user_id", "journey_count"])
        df_output = df_output = df_journeys.merge(
            df_output, left_index=True, right_index=True, how="inner"
        )
        df_output = df_output.reset_index()
        return df_output
