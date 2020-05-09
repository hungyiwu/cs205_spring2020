import os
import shutil

import tqdm

from pymatgen.ext.matproj import MPRester

if __name__ == '__main__':
    # make folder
    output_folderpath = './all_poscar'
    if os.path.isdir(output_folderpath):
        shutil.rmtree(output_folderpath)
    os.mkdir(output_folderpath)

    # open restful interface
    with MPRester(api_key='9bASScRXuQNDSebS') as m:
        # get material ID of all substrates
        matid_list = m.get_all_substrates()

        for matid in tqdm.tqdm(matid_list):
            try:
                s = m.get_structure_by_material_id(material_id=matid,
                        conventional_unit_cell=True)

                # convert to POSCAR string
                p = s.to(fmt='poscar')

                # save to disk
                output_filepath = os.path.join(output_folderpath,
                        '{}.poscar'.format(matid))
                with open(output_filepath, 'w') as outfile:
                    outfile.write(p)
            except:
                continue

