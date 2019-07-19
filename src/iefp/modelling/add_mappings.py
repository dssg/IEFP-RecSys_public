import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import yaml

from iefp.intermediate.transform_interventions import TransformInterventions


class AddModelMappings(luigi.Task):
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    s3path = buckets["modelling"]["map"]

    def requires(self):
        return TransformInterventions()

    def output(self):
        return S3Target(self.s3path + "final_mappings.parquet")

    def run(self):
        df_intermediate = pd.read_parquet(self.input().path)
        df_intermediate = self.add_mappings(df_intermediate)
        df_intermediate.to_parquet(self.output().path)

    def add_mappings(self, df):
        '''
        Function adds mappings for demographic features like school_qualification
        :param df: takes the transformed intermediate df as the input
        :return: returns the df with mappings applied to selected demographic features
        '''
        school_mappings = yaml.load(open("./conf/base/school_mappings.yml"),
                                    Loader=yaml.FullLoader)
        school_mappings = {str(key): value for key, value in school_mappings.items()}
        college_mappings = yaml.load(open("./conf/base/college_mappings.yml"),
                                     Loader=yaml.FullLoader)
        college_mappings = {str(key): value for key, value in college_mappings.items()}

        # Apply school mapping from Nova
        df['school_qualification'] = df['school_qualification'].map(school_mappings)

        # Apply college mapping from Nova
        df['college_qualification'] = df['college_qualification'].str[0].map(
                                                                college_mappings)

        # Apply boolean transformations
        df["disabled"] = df["disabled"] != 0.0
        df['subsidy'] = df['subsidy'].notna()

        return df
