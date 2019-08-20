import boto3
import pickle
import pyarrow as pa
import pyarrow.parquet as pq

from s3fs import S3FileSystem

from iefp.data import credentials


def write_parquet(df, s3path):
    table = pa.Table.from_pandas(df)
    s3fs = create_s3fs()
    pq.write_table(table=table, where=s3path, filesystem=s3fs)


def read_parquet(s3path):
    s3fs = create_s3fs()
    dataset = pa.parquet.ParquetDataset(s3path, filesystem=s3fs)
    return dataset.read_pandas().to_pandas()


def read_pickle(s3path):
    return pickle.loads(read_object(s3path))


def write_pickle(object_, s3path):
    write_object(pickle.dumps(object_), s3path)


def read_object(s3path):
    bucket, key = split_bucket_key(s3path)
    s3 = create_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def write_object(object_, s3path):
    bucket, key = split_bucket_key(s3path)
    s3 = create_client()
    s3.put_object(Bucket=bucket, Key=key, Body=object_)


def split_bucket_key(s3path):
    bucket = s3path.strip("s3://").split("/")[0]
    key = "/".join(s3path.strip("s3://").split("/")[1:])
    return bucket, key


def path(s3key):
    return "s3://{}/{}".format(bucket(), s3key)


def bucket():
    _, _, bucket = credentials.s3()
    return bucket


def create_client():
    key_id, secret, _ = credentials.s3()
    s3 = boto3.client("s3", aws_access_key_id=key_id, aws_secret_access_key=secret)
    return s3


def create_s3fs():
    key_id, secret, _ = credentials.s3()
    return S3FileSystem(key=key_id, secret=secret)
