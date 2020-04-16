import os

import pandas as pd

import util

if __name__ == '__main__':
    # paths
    poscar_folderpath = './all_poscar'
    query_filepath = './query_result.csv'
    survey_filepath = './survey_result.csv'

    # load data
    elementgroup_dict = util.element_of_interest()
    query_df = pd.read_csv(query_filepath)

    # survey element counts
    def get_counts(row):
        decomp = util.decomp_formula(row['pretty_formula'])
        TM = [t[1] for t in decomp if t[0] in\
                elementgroup_dict['transition_metal']]
        C = [t[1] for t in decomp if t[0] in\
                elementgroup_dict['chalcogen']]
        return len(TM), sum(TM), len(C), sum(C)

    query_df[['count_unique_TM', 'count_TM', 'count_unique_C', 'count_C']]\
            = query_df.apply(get_counts, axis=1, result_type='expand')

    # extract c-axis value
    def get_caxis(row):
        poscar_filepath = os.path.join(poscar_folderpath,
                '{}.poscar'.format(row['material_id']))
        with open(poscar_filepath, 'r') as infile:
            caxis = float(infile.readlines()[4].split()[2])
        return caxis

    query_df['caxis'] = query_df.apply(get_caxis, axis=1)

    # save to disk
    query_df.to_csv(survey_filepath, index=False)
