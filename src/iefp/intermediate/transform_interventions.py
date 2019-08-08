import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import numpy as np
import yaml

from iefp.intermediate import AddDemographics
from iefp.processing import CleanInterventions
from iefp.data.constants import Interventions


class TransformInterventions(luigi.Task):
    def requires(self):
        return [CleanInterventions(), AddDemographics()]

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        s3path = buckets["intermediate"]["transform"]

        return S3Target(s3path + "intermediate.parquet")

    def run(self):
        df_interventions = pd.read_parquet(self.input()[0].path).reset_index()
        df_interventions = self.group_efa(df_interventions)
        df_interventions = self.add_training(df_interventions)
        df_interventions = self.group_training(df_interventions)
        df_interventions = self.filter_interventions(df_interventions)
        df_journeys = pd.read_parquet(self.input()[1].path)
        df_output = self.transform_interventions(df_interventions, df_journeys)

        # Recount journeys, because we removed journeys in between
        df_output["journey_count"] = 1
        df_output["journey_count"] = df_output.groupby(["user_id"])[
            "journey_count"
        ].cumsum()
        df_output.to_parquet(self.output().path)

    def group_efa(self, df_interventions):
        """
        Function groups all EFA codes into one intervention

        :param df_interventions: cleaned panadas interventions dataframe
        :return: pandas dataframe
        """
        df_interventions.loc[
            (
                df_interventions.codigo_intervencao.isin(
                    Interventions.EFA_INTERVENTIONS_LIST
                )
            ),
            "codigo_intervencao",
        ] = Interventions.EFA_GENERIC_INTERVENTION
        return df_interventions

    def add_training(self, df_interventions):
        """
        Function breaks down training types in interventons table
        into separate interventions

        :param df_interventions: cleaned pandas interventions dataframe
        :return: pandas dataframe
        """
        df_777_training = df_interventions.loc[
            (df_interventions["codigo_intervencao"] == Interventions.TRAINING)
            & (df_interventions["f_cmod_form"].notna()),
        ]
        df_777_training.loc[:, "codigo_intervencao"] = str(
            Interventions.TRAINING
        ) + df_777_training.loc[:, "f_cmod_form"].astype(int).astype(str)

        df_777_training.loc[:, "codigo_intervencao"] = df_777_training.loc[
            :, "codigo_intervencao"
        ].astype(int)

        df_interventions.loc[df_777_training.index, :] = df_777_training.loc[
            df_777_training.index, :
        ]

        return df_interventions

    def group_training(self, df_interventions):
        """
        Function that groups types of training where few people have taken
        the training sub-category. Result is 1 generic training
        (where no sub category in data) and 4 main training sub-categories

        :param df_interventions: the outputted pandas dataframe from the
        add_training function
        :return: pandas dataframe
        """
        df_interventions.loc[
            (
                df_interventions["codigo_intervencao"].isin(
                    Interventions.TRAINING_SUB_CATEGORIES
                )
            ),
            "codigo_intervencao",
        ] = Interventions.GENERIC_TRAINING_SUB_CATEGORY
        return df_interventions

    def filter_interventions(self, df_interventions):
        """
        Function that filters for interventions which are 1. sucessful
        and that 2. iefp want to recommend.

        :param df_interventions: the interventions pandas dataframe
        :return: pandas dataframe
        """
        success = yaml.load(
            open("./conf/base/successful_intervention_results.yml"),
            Loader=yaml.FullLoader,
        )
        df_interventions = df_interventions[
            df_interventions["resultado_intervencao"].isin(success)
        ]

        recommendable_interventions = yaml.load(
            open("./conf/base/recommendable_interventions.yml"), Loader=yaml.FullLoader
        )
        df_interventions = df_interventions[
            df_interventions["codigo_intervencao"].isin(recommendable_interventions)
        ]

        return df_interventions

    def transform_interventions(self, df_interventions, df_journeys):
        """
        Function adds interventions which occur within a jouney to the journey
        pd.dataframe

        :param df_interventions: Cleaned and extracted interventions pd.dataframe
        :param df_journeys: Most recent journey pd.dataframe with outcomes
        (one line per jouney)
        :return: Returns the intermediate layer as a wide pd.dataframe with journey
        information, demographics, and outcomes and one date column for each
        intervention code
        """

        # Merge interventions with basic journey info
        df_interventions = df_interventions[
            ["ute_id", "data_intervencao", "codigo_intervencao"]
        ]
        df_interventions = df_interventions.set_index("ute_id")
        df_journeys = df_journeys.set_index("user_id")
        df_output = df_journeys[["journey_count", "register_date", "exit_date"]].merge(
            df_interventions, how="inner", left_index=True, right_index=True
        )

        # Filter for interventions that within a jouney
        df_output = df_output[
            (df_output["data_intervencao"] >= df_output["register_date"])
            & (df_output["data_intervencao"] <= df_output["exit_date"])
        ]
        df_output = df_output[
            ["journey_count", "data_intervencao", "codigo_intervencao"]
        ]
        df_output.columns = ["journey_count", "intervention_date", "intervention_code"]

        # Transform to one row per journey
        df_output = df_output.reset_index().rename(columns={"index": "user_id"})
        df_output = df_output = df_output.set_index(["user_id", "journey_count"])
        df_output["intervention_code"] = df_output["intervention_code"].astype(str)
        df_output = df_output.pivot_table(
            index=["user_id", "journey_count"],
            columns=["intervention_code"],
            aggfunc=np.min,
        )
        df_output.columns = ["_".join(col).strip() for col in df_output.columns.values]

        # Merge with full journey info
        df_journeys = df_journeys.reset_index().rename(columns={"index": "user_id"})
        df_journeys = df_journeys.set_index(["user_id", "journey_count"])
        df_output = df_journeys.merge(
            df_output, left_index=True, right_index=True, how="inner"
        )
        df_output = df_output.reset_index()
        return df_output
