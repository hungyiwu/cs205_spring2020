import json

import pandas as pd

if __name__ == '__main__':
    # paths
    cloud_filepath = 'compounds.json'
    poscar_filepath = '../query/selected_survey_result.csv'

    # parse 2D material list
    with open(cloud_filepath, 'r') as infile:
        d = json.load(infile)['data']['compounds']

    record = []
    for key in d:
        record.append({'formula': key, 'space_group': d[key]['space_group']})

    df_2d = pd.DataFrame.from_records(record)\
            .sort_values(['formula', 'space_group'])

    # load POSCAR list
    df_poscar = pd.read_csv(poscar_filepath)

    # merge
    df = df_2d.merge(df_poscar, left_on='formula', right_on='pretty_formula',
        how='inner')

    print(df.head())
