import boto3
import pickle


def read_object_from_s3(s3path):
    """
    Reades a pickle object from s3

    :param s3path: Full s3 path (e.g. "s3://iefp-unemployment/models/svm.pkl")
    :returns: Python object
    """
    s3 = boto3.client("s3")
    bucket = s3path.strip("s3://").split("/")[0]
    key = "/".join(s3path.strip("s3://").split("/")[1:])
    response = s3.get_object(Bucket=bucket, Key=key)
    return pickle.loads(response["Body"].read())


def write_object_to_s3(object_, s3path):
    """
    Writes any serializable pyhon object as pickle to specified s3path

    :param object_: Serializable python object
    :param s3path: Full s3 path (e.g. "s3://iefp-unemployment/models/svm.pkl")
    """
    s3 = boto3.client("s3")
    bucket = s3path.strip("s3://").split("/")[0]
    key = "/".join(s3path.strip("s3://").split("/")[1:])
    s3.put_object(Bucket=bucket, Key=key, Body=pickle.dumps(object_))
