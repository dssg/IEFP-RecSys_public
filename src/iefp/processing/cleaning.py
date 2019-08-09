import luigi
import numpy as np
import pandas as pd
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data.extract import ExtractPedidos, ExtractInterventions
from iefp.processing.constants import PedidosColumns, InterventionColumns


class CleanPedidos(luigi.Task):
    def requires(self):
        return ExtractPedidos()

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        target_path = buckets["intermediate"]["clean"]
        return S3Target(target_path + "pedidos.parquet")

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = clean(df, bool_cols=PedidosColumns.BOOLEAN)
        df.to_parquet(self.output().path)


class CleanInterventions(luigi.Task):
    def requires(self):
        return ExtractInterventions()

    def output(self):
        buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
        target_path = buckets["intermediate"]["clean"]
        return S3Target(target_path + "interventions.parquet")

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = clean(df, string_cols=InterventionColumns.STRING)
        df.to_parquet(self.output().path)


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
