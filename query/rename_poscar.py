import os
import shutil

if __name__ == '__main__':
    src_folderpath = 'ready_poscar'
    dst_folderpath = 'renamed_poscar'

    for filename in os.listdir(src_folderpath):
        src_filepath = os.path.join(src_folderpath, filename)
        with open(src_filepath, 'r') as infile:
            line = infile.readlines()[5].strip().split()
            new_name = 'POSCAR_{}{}2'.format(line[0], line[1])
        dst_filepath = os.path.join(dst_folderpath, new_name)
        shutil.copyfile(src_filepath, dst_filepath)
