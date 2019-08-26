from pathlib import Path
import yaml


def postgres():
    """
    Reads and return postgres credentials

    :return tuple: host, name, user, password, port
    """
    rootpath = Path(__file__).absolute().parents[3]
    path = rootpath / "conf/local/credentials.yml"
    cred = yaml.load(open(path), Loader=yaml.FullLoader)["db"]

    return (
        cred["pg_host"],
        cred["pg_name"],
        cred["pg_user"],
        cred["pg_pass"],
        cred["pg_port"],
    )


def s3():
    """
    Reads and return s3 credentials

    :return tuple: key_id, access_key, s3 bucket name
    """
    rootpath = Path(__file__).absolute().parents[3]
    path = rootpath / "conf/local/credentials.yml"
    creds = yaml.load(open(path), Loader=yaml.FullLoader)["aws"]
    return (
        creds["aws_access_key_id"],
        creds["aws_secret_access_key"],
        creds["s3_bucket_name"],
    )
