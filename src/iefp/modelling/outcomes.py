import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import yaml
import numpy as np

from iefp.modelling import AddMappings


class AddOutcomes(luigi.Task):
    def requires(self):
        return AddMappings()

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        target_path = buckets["modelling"]

        return S3Target(target_path + "modelling.parquet")

    def run(self):
        df_journeys = pd.read_parquet(self.input().path)
        df_journeys = self.add_bin_outcomes(df_journeys)
        df_journeys = self.add_ttj_outcomes(df_journeys)
        df_journeys.to_parquet(self.output().path)

    def add_bin_outcomes(self, df):
        """returns a journey dataframe with a boolean employment outcome"""

        outcome_mappings = yaml.load(
            open("./conf/base/successful_outcomes.yml"), Loader=yaml.FullLoader
        )["successful_outcomes"]

        df["success"] = df.exit_date_21.notna() | (
            df.exit_date_31.notna() & df.exit_reason.isin(outcome_mappings)
        )

        return df

    def add_ttj_outcomes(self, df):
        """returns a journey dataframe with a time-to-job boolean outcome"""

        exit31 = (df.exit_date_31 - df.register_date).dt.days
        exit21 = (df.exit_date_21 - df.register_date).dt.days
        df["ttj_sub_9"] = np.where(
            np.logical_or(exit21 < 270, np.logical_and(exit31 < 270, df.success)),
            True,
            False,
        )

        return df
