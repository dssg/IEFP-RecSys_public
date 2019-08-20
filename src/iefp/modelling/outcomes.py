import luigi
import numpy as np
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import Movement, S3
from iefp.modelling import AddMappings


class AddOutcomes(luigi.Task):
    def requires(self):
        return AddMappings()

    def output(self):
        return S3Target(s3.path(S3.MODELLING + "outcomes.parquet"))

    def run(self):
        df_journeys = s3.read_parquet(self.input().path)
        df_journeys = self.add_outcomes(df_journeys)
        s3.write_parquet(df_journeys, self.output().path)

    def add_outcomes(self, df):
        """returns a journey dataframe with a boolean employment outcome"""

        successful_outcomes = yaml.load(
            open("./conf/base/successful_outcomes.yml"), Loader=yaml.FullLoader
        )["successful_outcomes"]

        df["success"] = (df.exit_movement == Movement.JOB_PLACEMENT_IEFP) | (
            (df.exit_movement == Movement.CANCELLATION)
            & df.exit_reason.isin(successful_outcomes)
        )

        df["journey_length"] = df.exit_date - df.register_date
        df["journey_length"] = np.ceil(df["journey_length"] / np.timedelta64(1, "D"))

        return df
