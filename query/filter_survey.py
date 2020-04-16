import os
import shutil

import pandas as pd

if __name__ == '__main__':
    # paths
    poscar_folderpath = './all_poscar'
    dest_folderpath = './selected_poscar'
    survey_filepath = './survey_result.csv'
    output_filepath = './selected_survey_result.csv'

    if os.path.isdir(dest_folderpath):
        shutil.rmtree(dest_folderpath)
    os.mkdir(dest_folderpath)

    # filter
    survey_df = pd.read_csv(survey_filepath)
    mask = (survey_df['count_unique_TM'] == 1)\
            & (survey_df['count_TM'] == 1)\
            & (survey_df['count_unique_C'] <= 2)\
            & (survey_df['count_C'] == 2)\
            & (survey_df['caxis'] > 15)

    # save selected table
    survey_df.loc[mask].to_csv(output_filepath, index=False)

'''
need to solve duplicating consensus formula issue
    # copy POSCAR files
    for index in survey_df.index[mask]:
        src_filepath = os.path.join(poscar_folderpath,
                '{}.poscar'.format(survey_df.loc[index, 'material_id']))
        dst_filepath = os.path.join(dest_folderpath,
                'POSCAR_{}'.format(survey_df.loc[index, 'consensus_formula']))
        shutil.copyfile(src=src_filepath, dst=dst_filepath)
'''
