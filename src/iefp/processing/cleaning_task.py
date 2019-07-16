import luigi
from luigi.contrib.s3 import S3Target
import yaml
import pandas as pd
import numpy as np

from iefp import processing
from iefp.data.extract import ExtractPedidos, ExtractInterventions


class CleanPedidos(luigi.Task):
    ped_cols = yaml.load(
        open("./conf/base/pedidos_col_types.yml"), Loader=yaml.FullLoader
    )
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    s3path = buckets["intermediate"]["clean"]

    # Load parameters
    bool_list = ped_cols["bool_list"]
    date_list = ped_cols["date_list"]
    dirty_string_list = ped_cols["dirty_string_list"]
    object_date_list = ped_cols["object_date_list"]

    def requires(self):
        return ExtractPedidos()

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = clean(self, df)
        df.to_parquet(self.output().path)

    def output(self):
        return S3Target(self.s3path + "pedidos.parquet")


class CleanInterventions(luigi.Task):

    interv_cols = yaml.load(
        open("./conf/base/interventions_col_types.yml"), Loader=yaml.FullLoader
    )
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    s3path = buckets["intermediate"]["clean"]

    # Load parameters
    bool_list = interv_cols["bool_list"]
    date_list = interv_cols["date_list"]
    dirty_string_list = interv_cols["dirty_string_list"]
    object_date_list = interv_cols["object_date_list"]

    def requires(self):
        return ExtractInterventions()

    def run(self):
        df = pd.read_parquet(self.input().path)
        df = clean(self, df)
        df.to_parquet(self.output().path)

    def output(self):
        return S3Target(self.s3path + "interventions.parquet")


def clean(self, df):
    # Check if there are dirty strings and clean if present
    if self.dirty_string_list:
        df[self.dirty_string_list] = processing.clean_string(df[self.dirty_string_list])

    # Check if there are objects which should be dates and convert if present
    if self.object_date_list:
        for col in self.object_date_list:
            df[col] = processing.object_to_date(df[col], "%Y-%m-%d %H:%M:%S")

    # Replace all None types with Pandas NaNs
    df = df.replace(to_replace=[None], value=np.nan)
    df = df.replace(to_replace="  ", value=np.nan)

    # Convert all appropriate column datatypes to int
    df_float = df.select_dtypes(exclude=["datetime"])
    df_int = df_float.apply(pd.to_numeric, errors="ignore", downcast="integer")
    df[df_int.columns] = df_int[df_int.columns]

    # Boolean convert
    if self.bool_list:
        df = processing.bool_convert(df, self.bool_list)

    # Strip time from datetime columns
    if self.date_list:
        df = processing.strip_time(df, self.date_list)

    # Remove duplicates
    df = df.drop_duplicates()

    return df
