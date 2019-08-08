import yaml


def get_postgres_credentials():
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
