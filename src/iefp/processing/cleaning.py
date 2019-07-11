import pandas as pd


def clean_string(column):
    "function to make string column lower case and remove characters defined in list"
    column = column.str.lower()
    characters = ['(', ')', '-', '+', '  ']
    for char in characters:
        column = column.str.replace(char, "", case=False, regex=False)

    return column


def object_to_date(column, inputformat):
    """converts object column to string, then to datetime, then to date"""
    column = column.astype("int64").astype("str")
    column = pd.to_datetime(column, errors='coerce', format=inputformat)
    column = column.dt.date
    return column


def bool_convert(dataframe, bool_list):
    bool_dict = {"S": 1, "N": 0}
    for col in bool_list:
        dataframe[col] = dataframe[col].map(bool_dict)
        dataframe[col] = dataframe[col].astype(bool)
    return dataframe


def strip_time(dataframe, date_list):
    for date_col in date_list:
        dataframe[date_col] = pd.to_datetime(dataframe[date_col].dt.date)
    return dataframe
