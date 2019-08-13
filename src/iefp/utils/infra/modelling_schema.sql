DROP SCHEMA IF EXISTS modelling;

CREATE SCHEMA modelling;

--table evaluations: where we store all the different models that we've tried
DROP TABLE IF EXISTS modelling.evaluations;

CREATE TABLE modelling.evaluations(
    model_id serial,
    model_type varchar,
    features varchar[],
    hyperparameters json,
    execution_time float,
    date_run timestamp with time zone,
    m_precision float,
    m_recall float,
    m_f1 float,
    m_accuracy float,
    m_baserate integer,
    train_data_path varchar,
    test_data_path varchar,
    model_path varchar,
    primary key(model_id)
);

CREATE INDEX evaluations_pkey on evaluations(model_id);
