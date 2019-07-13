import pandas as pd


def clean_string(df):
    """function to make string column lower case and remove characters defined in list"""
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    characters = ['(', ')', '-', '+', '  ', '.']
    for char in characters:
        df = df.apply(lambda s: s.replace(char, "", regex=False))
    return df


def object_to_date(column, inputformat):
    """converts object column to string, then to datetime, then to date"""
    column = column.astype("int64").astype("str")
    column = pd.to_datetime(column, errors='coerce', format=inputformat)
    column = column.dt.date
    return column


def bool_convert(dataframe, bool_list):
    """maps yes/no fields to 1/0 and then converts to boolean"""
    bool_dict = {"S": 1, "N": 0}
    for col in bool_list:
        dataframe[col] = dataframe[col].map(bool_dict)
        dataframe[col] = dataframe[col].astype(bool)
    return dataframe


def strip_time(dataframe, date_list):
    """strips time element from datetime columns"""
    for date_col in date_list:
        dataframe[date_col] = pd.to_datetime(dataframe[date_col].dt.date)
    return dataframe
