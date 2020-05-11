import os
import itertools

import numpy as np
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

    # extract info from formula
    # atom counts, consensus formula
    def parse_formula(row):
        decomp = util.decomp_formula(row['formula'])
        TM = [t for t in decomp if t[0] in elementgroup_dict['transition_metal']]
        C = [t for t in decomp if t[0] in elementgroup_dict['chalcogen']]

        # get counts
        count_uTM, count_TM = len(TM), sum([t[1] for t in TM])
        count_uC, count_C = len(C), sum([t[1] for t in C])

        # construct consensus formula
        TM = sorted(TM, key=lambda t: t[0]) # sort by alphabetical order
        C = sorted(C, key=lambda t: t[0]) # sort by alphabetical order
        species_list = []
        for t in itertools.chain(TM, C):
            if t[1] > 1:
                species = t[0]+str(int(t[1]))
            else:
                species = t[0]
            species_list.append(species)
        consensus_formula = ''.join(species_list)
        return count_uTM, count_TM, count_uC, count_C, consensus_formula

    query_df[['count_unique_TM', 'count_TM', 'count_unique_C', 'count_C',
        'consensus_formula']] = query_df.apply(parse_formula, axis=1, result_type='expand')

    # extract info from POSCAR file
    # c-axis value, symmetry angle
    def parse_poscar(row):
        poscar_filepath = os.path.join(poscar_folderpath,
                '{}.poscar'.format(row['material_id']))
        with open(poscar_filepath, 'r') as infile:
            lines = infile.readlines()

            vec_a = np.array([float(s) for s in lines[2].split()])
            vec_b = np.array([float(s) for s in lines[3].split()])
            ua = vec_a / np.linalg.norm(vec_a)
            ub = vec_b / np.linalg.norm(vec_b)
            angle = np.arccos(np.dot(ua, ub)) # radian
            angle = np.degrees(angle) # degrees

            caxis = float(lines[4].split()[2])

        return angle, caxis

    query_df[['ab_angle(degree)', 'caxis']] = query_df.apply(parse_poscar, axis=1,
            result_type='expand')

    # save to disk
    query_df.to_csv(survey_filepath, index=False)
