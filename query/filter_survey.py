import os
import shutil

import numpy as np
import pandas as pd

if __name__ == '__main__':
    # paths
    poscar_folderpath = './all_poscar'
    formula_filepath = '2D_material_list.csv'
    dest_folderpath = './selected_poscar'
    survey_filepath = './survey_result.csv'
    output_filepath = './selected_survey_result.csv'

    # load data
    formula_df = pd.read_csv(formula_filepath)
    survey_df = pd.read_csv(survey_filepath)

    # filter by formula and space group
    survey_df = survey_df.merge(formula_df, on=['formula', 'space_group'],
            how='inner')

    # filter by atom counts
    mask = (survey_df['count_unique_TM'] == 1)\
            & (survey_df['count_unique_C'] <= 2)
    survey_df = survey_df.loc[mask]

    # filter by lattice shape
    degree_target = [59, 60, 61, 119, 120, 121]
    mask = survey_df['ab_angle(degree)'].apply(lambda x: int(np.round(x)) in degree_target)
    survey_df = survey_df.loc[mask]

    # label with "good as-is" or "need to extract mono-layer"
    mask = (survey_df['count_TM'] == 1)\
            & (survey_df['count_C'] == 2)\
            & (survey_df['nsites'] == 3)
    survey_df['mono_layer'] = mask

    # save selected table
    survey_df.sort_values('consensus_formula')\
            .to_csv(output_filepath, index=False)
