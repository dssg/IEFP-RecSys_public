import luigi
from luigi.contrib.s3 import S3Target
from sqlalchemy import create_engine
import yaml
import pandas as pd


class ExtractPedidos(luigi.Task):

    s3path = "s3://iefp-unemployment/intermediate/filter/pedidos.parquet"
    sigae_cols = yaml.load(open("./conf/base/sigae_columns.yml"), Loader=yaml.FullLoader)

    table = "pedidos"
    cols = sigae_cols["pedidos"]
    limit = 5000000

    query = """
    select {}
    from {}
    order by ano_mes desc
    limit {}
    """.format(
        ", ".join(cols), table, limit
    )

    def run(self):
        query_to_parquet(self.query, self.s3path)

    def output(self):
        return S3Target(self.s3path)


def query_to_parquet(query, s3path):
    creds = yaml.load(open("./conf/local/credentials.yml"), Loader=yaml.FullLoader)
    pg_cred = creds["db"]

    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(
        pg_cred["pg_user"], pg_cred["pg_pass"], pg_cred["pg_host"], 5432, "iefp"
    )
    con = create_engine(url, client_encoding="utf8")

    df = pd.read_sql(query, con)
    df.to_parquet(s3path, compression="snappy")
