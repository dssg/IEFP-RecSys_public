def translate_columns(tables, trans_dict):
    '''Function to translate column names for a list of tables'''
    for df_table in tables:
        df_table.rename(columns=trans_dict, inplace=True)

    return tables
