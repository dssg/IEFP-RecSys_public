import luigi
import pandas as pd
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import S3
from iefp.modelling import AddOutcomes


class CreateModellingTable(luigi.Task):
    def requires(self):
        return AddOutcomes()

    def output(self):
        return S3Target(s3.path(S3.MODELLING + "modelling.parquet"))

    def run(self):
        df_journeys = s3.read_parquet(self.input().path)
        df_journeys = df_journeys.set_index(["user_id", "journey_count"])

        df_interventions = self.dummy_interventions(df_journeys)
        df_feats = self.transform_features(df_journeys)

        df_model = df_feats.merge(df_interventions, right_index=True, left_index=True)

        # NOTE: Cut-off modeling table at specified time.
        modelling_params = yaml.load(
            open("./conf/base/parameters.yml"), Loader=yaml.FullLoader
        )
        df_model = df_model[
            df_model["register_date"] >= modelling_params["data_set"]["start"]
        ].reset_index()

        df_model = df_model.drop(["user_id", "register_date"], axis="columns")
        df_model = self.drop_empty_cols(df_model)
        df_model = self.set_target_variables(df_model)

        s3.write_parquet(df_model, self.output().path)

    def drop_empty_cols(self, df_model):
        """
        Drops columns with only one distinct value, since they bare no information

        :param df: Modelling dataframe
        :return: Modelling dataframe
        """
        nunique = df_model.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        df_model = df_model.drop(cols_to_drop, axis="columns")
        return df_model

    def set_target_variables(self, df_model):
        """
        Set time-to-job and time-to-job within 12 month as target variables

        :param df: Modelling dataframe
        :return: Modelling dataframe
        """
        df_model["ttj_sub_12"] = (df_model["journey_length"] < 365) & (
            df_model["success"] == True
        )

        df_model["ttj"] = df_model.loc[df_model["success"] == True, "journey_length"]

        df_model = df_model.drop(["journey_length", "success"], axis="columns")
        return df_model

    def dummy_interventions(self, df):
        """
        Transforms interventions to binary representation instead of dates.

        :param df: Journey dataframe
        :return: Binarized interventions dataframe
        """
        interv_cols = [col for col in df.columns if "i_" in col]
        df = df[interv_cols]
        df = (df.notna()).astype(int)

        return df

    def transform_features(self, df):
        """
        Selects and transforms demographic features instead of dates.

        :param df: Journey dataframe
        :return: Feature dataframe
        """
        dems = [
            "d_age",
            "d_civil_status",
            "d_college_qualification",
            "d_desired_contract",
            "d_desired_job_sector",
            "d_desired_work_time",
            "d_disabled",
            "d_gender",
            "d_nationality",
            "d_previous_job_sector",
            "d_rsi",
            "d_school_qualification",
            "d_subsidy",
        ]
        # NOTE: Keep exit_date for now since we use it to split into train and test
        # in a later task.
        feats = ["register_date", "register_reason", "exit_date"]
        outcomes = ["journey_length", "success"]
        df_feats = df.loc[:, dems + feats + outcomes]

        df_feats["register_month"] = df_feats["register_date"].dt.month.astype(
            "category"
        )
        df_feats["register_year"] = df_feats["register_date"].dt.year.astype("category")

        df_feats["register_reason"] = df_feats["register_reason"].astype("category")
        df_feats["d_school_qualification"] = df_feats["d_school_qualification"].astype(
            "category"
        )

        df_feats = pd.get_dummies(df_feats, drop_first=True, dummy_na=True)

        return df_feats
