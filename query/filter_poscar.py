import os
import shutil

from pymatgen.core import periodic_table, composition

if __name__ == '__main__':
    # paths
    source_folderpath = './all_poscar'
    dest_folderpath = './TMDC_poscar'

    # params
    caxis_threshold = 15

    # prepare destination folder
    if os.path.isdir(dest_folderpath):
        shutil.rmtree(dest_folderpath)
    os.mkdir(dest_folderpath)

    # iterate
    for filename in os.listdir(source_folderpath):
        # extract properties
        filepath = os.path.join(source_folderpath, filename)
        with open(filepath, 'r') as infile:
            lines = infile.readlines()
            comp_list = lines[0].strip().split()
            element_list = lines[5].strip().split()
            caxis = float(lines[4].strip().split()[2])

        # c-axis threshold
        if caxis < caxis_threshold:
            continue

        # parse element by groups
        element_dict = {'transition_metal': [], 'chalcogen': [], 'others': []}
        for element_str in element_list:
            group = periodic_table.Element[element_str].group
            if group == 16:
                element_dict['chalcogen'].append(element_str)
            elif group >= 3 and group <= 12:
                element_dict['transition_metal'].append(element_str)
            else:
                element_dict['others'].append(element_str)

        # filter by formula
        if len(element_dict['transition_metal']) != 1:
            continue
        if len(element_dict['chalcogen']) < 1 or\
                len(element_dict['chalcogen']) > 2:
            continue
        if len(element_dict['others']) > 0:
            continue

        # copy file
        comp_str = composition.Composition(''.join(comp_list)).reduced_formula
        shutil.copyfile(src=filepath, dst=os.path.join(dest_folderpath,
            'POSCAR_{}'.format(''.join(comp_str))))
