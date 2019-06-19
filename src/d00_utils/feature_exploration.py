def preview_all_data(table_dict, filename, save_to_file=False):
    '''preview_all_data loops over all columns in each dataframe and prints
     the column name and 3 non-nan values if they exist'''
    with open(filename, 'w') as data_sample:

        for table in table_dict:
            for j in range(len(table_dict[table].columns)):
                values = []
                for k in range(len(table_dict[table])):
                    table_dict[table].iloc[k:k+1, j:j+1].isnull().values.any()
                    if not table_dict[table].iloc[k:k+1, j:j+1].isnull().values.any():
                        values.append(
                            str(table_dict[table].iloc[k:k+1, j:j+1].values[0][0]))
                if save_to_file:
                    data_sample.writelines(
                        str(table_dict[table].columns[j]) + ': '
                        + ', '.join(values[0:3]) + '\n')
                print(
                    str(table_dict[table].columns[j]) + ': '
                    + ', '.join(values[0:3]) + '\n')
