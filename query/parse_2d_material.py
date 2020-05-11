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

    df_2d.to_csv('2D_material_list.csv', index=False)
