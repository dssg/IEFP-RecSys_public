import luigi
import numpy as np

from luigi.contrib.s3 import S3Target

from iefp.data import s3
from iefp.data.constants import S3
from iefp.data.extract import ExtractPedidos, ExtractInterventions
from iefp.processing.constants import PedidosColumns, InterventionColumns


class CleanPedidos(luigi.Task):
    def requires(self):
        return ExtractPedidos()

    def output(self):
        return S3Target(
            s3.path(S3.CLEAN + "pedidos.parquet"), client=s3.create_client()
        )

    def run(self):
        df = s3.read_parquet(self.input().path)
        df = clean(df, bool_cols=PedidosColumns.BOOLEAN)
        s3.write_parquet(df, self.output().path)


class CleanInterventions(luigi.Task):
    def requires(self):
        return ExtractInterventions()

    def output(self):
        return S3Target(
            s3.path(S3.CLEAN + "interventions.parquet"), client=s3.create_client()
        )

    def run(self):
        df = s3.read_parquet(self.input().path)
        df = clean(df, string_cols=InterventionColumns.STRING)
        s3.write_parquet(df, self.output().path)


def clean(df, bool_cols=None, string_cols=None):
    """
    General cleaning workflow for different columns types

    :param df: DataFrame
    :param bool_cols: List of boolean columns with S/N instead of T/F
    :param string_cols: List of string columns that should be cleaned
    :return: Cleaned DataFrame
    """
    if string_cols:
        df[string_cols] = clean_string(df[string_cols])

    if bool_cols:
        df = bool_convert(df, bool_cols)

    df = df.replace("  ", " ").replace(" ", np.nan)
    df = df.replace([None], np.nan)
    df = df.drop_duplicates()
    return df


def clean_string(df):
    """
    Cleans string columns of dataframe


    :param df: DataFrame with string columns
    :return: Cleaned DataFrame
    """
    characters = ["(", ")", "-", "+", "."]
    for char in characters:
        df = df.apply(
            lambda s: s.str.strip().str.lower().replace(char, "", regex=False)
        )

    return df


def bool_convert(df, bool_list):
    """
    Maps S(im) N(ao) fields to True and False


    :param bool_list: List of S/N boolean columns
    :return: Converted DataFrame
    """
    bool_dict = {"S": True, "N": False}
    for col in bool_list:
        df[col] = df[col].map(bool_dict)
    return df
