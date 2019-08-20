import yaml


def postgres():
    """
    Reads and return postgres credentials

    :return tuple: host, name, user, password, port
    """
    cred = yaml.load(open("./conf/local/credentials.yml"), Loader=yaml.FullLoader)["db"]

    return (
        cred["pg_host"],
        cred["pg_name"],
        cred["pg_user"],
        cred["pg_pass"],
        cred["pg_port"],
    )


def s3():
    credentials = yaml.load(
        open("./conf/local/credentials.yml"), Loader=yaml.FullLoader
    )["aws"]
    return (
        credentials["aws_access_key_id"],
        credentials["aws_secret_access_key"],
        credentials["s3_bucket_name"],
    )
