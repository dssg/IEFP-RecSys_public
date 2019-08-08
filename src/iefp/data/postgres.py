import json

from sqlalchemy import create_engine

from iefp.data import get_postgres_credentials
from iefp.data.constants import Database


def get_db_engine():
    """
    Creates sqlalchemy database engine

    :return: Database engine
    """
    host, name, user, password, port = get_postgres_credentials()
    url = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, name)
    engine = create_engine(url, client_encoding="utf8")

    return engine


def get_best_model_path(metric="f1"):
    """
    Queries database for the best mode

    :param query: Evaluation metric as string:
        'f1', 'accuracy', 'precision', 'recall'
    :return: S3path of model location
    """
    table = Database.EVALUATION_TABLE
    query = """
    select file_path
    from {}
    order by {}
    limit 1
    """.format(
        table, "m_{}".format(metric)
    )

    res = query_db(query)
    return res.first()[0]


def query_db(query):
    """
    Executes an sql string query

    :param query: string query
    :return: resultset as list of tuples
    """
    engine = get_db_engine()
    with engine.connect() as con:
        return con.execute(query)


def model_info_to_db(engine, model, metrics, features, date, filepath):
    """
    Writes model information including evaluation metrics to evaluation table

    :param engine: Sqlalchemy database engine
    :param model: Trained scikit-learn model
    :param metrics: Dictionary of evaluation metrics in the form of
        metrics = {
            "m_accuracy": accuracy,
            "m_f1": f1,
            "m_precision": precision,
            "m_recall": recall,
        }
    :param features: List of feature names
    :param date: Datetime of model training
    :param filepath: S3 Filepath where the model file is stored
    """
    table = Database.EVALUATION_TABLE
    data = {
        "model_type": type(model).__name__,
        "features": str(features).replace("'", '"').replace("[", "{").replace("]", "}"),
        "hyperparameters": json.dumps(model.get_params()),
        "date_run": date,
        "file_path": filepath,
    }
    data.update(metrics)

    query = """
    insert into {} ({})
    values ('{}')
    """.format(
        table,
        ", ".join([str(v) for v in data.keys()]),
        "', '".join([str(v) for v in data.values()]),
    )

    query_db(query)
