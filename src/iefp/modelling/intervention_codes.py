import luigi
from luigi.contrib.s3 import S3Target
import pandas as pd
import yaml

from iefp.intermediate import TransformInterventions


class TranslateInterventions(luigi.Task):
    def requires(self):
        return TransformInterventions()

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        s3path = buckets["modelling"]

        return S3Target(s3path + "intervention_translate.parquet")

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = self.translate_intervention_codes(df)
        df.to_parquet(self.output().path)

    def translate_intervention_codes(self, df):
        """
        Function to take in the intermediate layer and rename the columns
        which have an intervention code in them to the translated description
        of the intervention
        :param df: Pandas dataframe
        :return: Pandas dataframe
        """
        code_dict = yaml.load(open("./conf/base/intervention_translation_dict.yml"))
        df.columns = [col.replace("intervention_date_", "") for col in df.columns]
        code_dict = {str(key): code_dict[key] for key in code_dict}
        df = df.rename(columns=code_dict)
        return df