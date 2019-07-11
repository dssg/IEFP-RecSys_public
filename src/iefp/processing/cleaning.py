import pandas as pd


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
