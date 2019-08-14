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


def get_best_model_paths(metric="f1"):
    """
    Queries database for the best mode

    :param query: Evaluation metric as string:
        'f1', 'accuracy', 'precision', 'recall'
    :return tuple: S3path of model, train_set, test_set
    """
    table = Database.EVALUATION_TABLE
    query = """
    select model_path, train_data_path, test_data_path
    from {}
    order by ({}, date_run) desc
    limit 1
    """.format(
        table, "m_{}".format(metric)
    )

    res = query_db(query)
    return res.first()[:3]


def query_db(query):
    """
    Executes an sql string query

    :param query: string query
    :return: resultset as list of tuples
    """
    engine = get_db_engine()
    with engine.connect() as con:
        return con.execute(query)


def model_info_to_db(
    engine, model, metrics, features, date, model_path, train_data_path, test_data_path
):
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
        "model_path": model_path,
        "train_data_path": train_data_path,
        "test_data_path": test_data_path,
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


def rec_eval_info_to_db(engine, error, model_id, parameters):
    """
    Writes model information including evaluation metrics to evaluation table

    :param engine: Sqlalchemy database engine
    :param error: Trained scikit-learn model
    :param model_id: List of feature names
    :param parameters: Dictionary of evaluation parameters in the form of
        parameters = {
        
        set_size = parameters["set_size"]
        num_recs = parameters["num_recs"]
        percent_sample = parameters["percent_sample"]
        
            "set_size": recommendation set size,
            "num_recs": number of recommendation sets returned,
            "percent_sample": percentage of the sample we evaluate recommendations for
        }
    """

    table = Database.RECOMMENDATION_ERRORS_TABLE
    data = {"model_id": model_id, "error": error, "parameters": json.dumps(parameters)}

    query = """
    insert into {} ({})
    values ({}, {}, '{}')
    """.format(
        table,
        ", ".join([str(v) for v in data.keys()]),
        model_id,
        error,
        json.dumps(parameters),
    )

    query_db(query)
