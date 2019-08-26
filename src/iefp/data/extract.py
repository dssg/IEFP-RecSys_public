import luigi
import pandas as pd
import yaml

from luigi.contrib.s3 import S3Target

from iefp.data.constants import Database, S3
from iefp.data import get_db_engine
from iefp.data import s3


class ExtractPedidos(luigi.Task):
    def run(self):
        sigae_cols = yaml.load(
            open("./conf/base/sigae_columns.yml"), Loader=yaml.FullLoader
        )

        table = Database.PEDIDOS_TABLE
        limit = Database.PEDIDOS_EXTRACTION_SIZE

        query = """
        select {}
        from {}
        where {}.tipo_movimento in (11, 31, 21, 43)
        order by ano_mes desc
        limit {}
        """.format(
            ", ".join(sigae_cols[table]), table, table, limit
        )

        paths = query_to_parquet(query, self.output().path, chunksize=limit / 10)
        concat_parquet(paths, self.output().path)

    def output(self):
        return S3Target(
            s3.path(S3.EXTRACT + "pedidos.parquet"), client=s3.create_client()
        )


class ExtractInterventions(luigi.Task):
    def run(self):
        sigae_cols = yaml.load(
            open("./conf/base/sigae_columns.yml"), Loader=yaml.FullLoader
        )

        table = Database.INTERVENTIONS_TABLE
        limit = Database.INTERVENTIONS_EXTRACTION_SIZE

        query = """
        select {}
        from {}
        where (({}.tipo_movimento = 35) and ({}.estado = 'ACT'))
        order by ano_mes desc
        limit {}
        """.format(
            ", ".join(sigae_cols[table]), table, table, table, limit
        )

        paths = query_to_parquet(query, self.output().path, chunksize=limit / 10)
        concat_parquet(paths, self.output().path)

    def output(self):
        return S3Target(
            s3.path(S3.EXTRACT + "interventions.parquet"), client=s3.create_client()
        )


def concat_parquet(paths, s3path):
    dfs = []
    for path in paths:
        df = s3.read_parquet(path)
        # NOTE: Convert to datetime seconds because the parquet
        # engine can not handle datetime nanoseconds.
        df_dates = df.select_dtypes("datetime")
        df_dates = df_dates.astype("datetime64[s]")
        df[df_dates.columns] = df_dates
        dfs.append(df)

    df = pd.concat(dfs)
    s3.write_parquet(df, s3path)


def query_to_parquet(query, s3path, chunksize):
    engine = get_db_engine()

    files = list()
    i = 0
    for chunk in pd.read_sql(query, engine, chunksize=chunksize):
        chunk_path = s3path.split(".")[0] + "_chunk{}.parquet".format(i)
        s3.write_parquet(chunk, chunk_path)
        files.append(chunk_path)
        i = i + 1

    return files
