import os
import shutil

import pandas as pd
import tqdm

from pymatgen.ext import matproj

if __name__ == '__main__':
    # path
    query_filepath = './query_result.csv'
    output_folderpath = './all_poscar'

    # make folder
    if os.path.isdir(output_folderpath):
        shutil.rmtree(output_folderpath)
    os.mkdir(output_folderpath)

    # open restful interface
    matid_list = pd.read_csv(query_filepath)['material_id'].tolist()
    with matproj.MPRester(api_key='9bASScRXuQNDSebS') as m:
        for matid in tqdm.tqdm(matid_list):
            s = m.get_structure_by_material_id(material_id=matid,
                    conventional_unit_cell=True)
            p = s.to(fmt='poscar')
            output_filepath = os.path.join(output_folderpath, '{}.poscar'.format(matid))
            with open(output_filepath, 'w') as outfile:
                outfile.write(p)
