import luigi
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import S3
from iefp.modelling import TranslateInterventions


class AddMappings(luigi.Task):
    def requires(self):
        return TranslateInterventions()

    def output(self):
        return S3Target(
            s3.path(S3.MODELLING + "mappings.parquet"), client=s3.create_client()
        )

    def run(self):
        df_intermediate = s3.read_parquet(self.input().path)
        df_intermediate = self.add_mappings(df_intermediate)
        s3.write_parquet(df_intermediate, self.output().path)

    def add_mappings(self, df):
        """
        Add mappings for demographic features with large number categories

        :param df: takes the transformed intermediate df as the input
        :return: returns the df with mappings applied to selected demographic features
        """
        college_mappings = yaml.load(
            open("./conf/base/college_mappings.yml"), Loader=yaml.FullLoader
        )
        college_mappings = {str(key): value for key, value in college_mappings.items()}
        # NOTE: Take first digit of college qualification for mapping
        df["d_college_qualification"] = (
            df["d_college_qualification"].str[0].map(college_mappings)
        )

        school_mappings = yaml.load(
            open("./conf/base/school_mappings.yml"), Loader=yaml.FullLoader
        )
        school_mappings = {
            ("0" + str(key) if len(str(key)) == 1 else str(key)): (value)
            for key, value in school_mappings.items()
        }
        df["d_school_qualification"] = df["d_school_qualification"].map(school_mappings)

        # NOTE: Take first digit of cpp for mapping
        cpp_mappings = yaml.load(
            open("./conf/base/cpp_mappings.yml"), Loader=yaml.FullLoader
        )
        df["d_desired_job_sector"] = (
            df.d_desired_cpp.dropna().astype(str).str[0].astype(int).map(cpp_mappings)
        )
        df["d_previous_job_sector"] = (
            df.d_previous_cpp.dropna().astype(str).str[0].astype(int).map(cpp_mappings)
        )
        df = df.drop(columns=["d_desired_cpp", "d_previous_cpp"])

        # Apply boolean transformations
        df["d_disabled"] = df["d_disabled"] != 0.0
        df["d_subsidy"] = df["d_subsidy"].notna()
        df.loc[df["d_nationality"] != "PT", "d_nationality"] = "other"

        return df
