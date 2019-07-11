import luigi
from luigi.contrib.s3 import S3Target
from sqlalchemy import create_engine
import yaml
import pandas as pd


class ExtractPedidos(luigi.Task):

    sigae_cols = yaml.load(open("./conf/base/sigae_columns.yml"), Loader=yaml.FullLoader)
    buckets = yaml.load(open("./conf/base/buckets.yml"), Loader=yaml.FullLoader)
    s3path = buckets["intermediate"]["filter"]

    table = "pedidos"
    cols = sigae_cols["pedidos"]
    limit = 10000000

    query = """
    select {}
    from {}
    order by ano_mes desc
    limit {}
    """.format(
        ", ".join(cols), table, limit
    )

    def run(self):
        paths = query_to_parquet(self.query, self.s3path, self.limit)
        concat_parquet(paths, self.output().path)

    def output(self):
        return S3Target(self.s3path + "pedidos.parquet")


def concat_parquet(paths, s3path):
    dfs = []
    for file in paths:
        df = pd.read_parquet(file)
        df_dates = df.select_dtypes("datetime")
        df_dates = df_dates.astype("datetime64[s]")
        df[df_dates.columns] = df_dates
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_parquet(s3path)


def query_to_parquet(query, s3path, rows):
    creds = yaml.load(open("./conf/local/credentials.yml"), Loader=yaml.FullLoader)
    pg_cred = creds["db"]

    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(
        pg_cred["pg_user"], pg_cred["pg_pass"], pg_cred["pg_host"], 5432, "iefp"
    )
    con = create_engine(url, client_encoding="utf8")

    files = list()
    i = 0
    for chunk in pd.read_sql(query, con, chunksize=rows / 10):
        temp_path = s3path + "temp{}.parquet".format(i)
        chunk.to_parquet(temp_path)
        files.append(temp_path)
        i = i + 1

    return files
