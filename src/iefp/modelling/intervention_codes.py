import luigi
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import S3
from iefp.intermediate import TransformInterventions


class TranslateInterventions(luigi.Task):
    def requires(self):
        return TransformInterventions()

    def output(self):
        return S3Target(
            s3.path(S3.TRANSFORM + "interventions_translated.parquet"),
            client=s3.create_client(),
        )

    def run(self):
        df = s3.read_parquet(self.input().path)
        df = self.translate_intervention_codes(df)
        s3.write_parquet(df, self.output().path)

    def translate_intervention_codes(self, df):
        """
        Function to take in the intermediate layer and rename the columns
        which have an intervention code in them to the translated description
        of the intervention
        :param df: Pandas dataframe
        :return: Pandas dataframe
        """
        code_dict = yaml.load(
            open("./conf/base/intervention_translation_dict.yml"),
            Loader=yaml.FullLoader,
        )
        df.columns = [col.replace("intervention_date_", "") for col in df.columns]
        code_dict = {str(key): code_dict[key] for key in code_dict}
        df = df.rename(columns=code_dict)
        return df
