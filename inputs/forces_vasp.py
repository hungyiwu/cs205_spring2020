import os
import sys
import re
import shutil

# params
#vasp_filepath, run_filepath = sys.argv[1], sys.argv[2]
misc_filename_list = ['POTCAR', 'KPOINTS']

phonopy_dir = '/n/holyscratch01/cs205/group4/example-ff/'
master_dir = os.getcwd()

#read supercell dimensions from phonopy parameters file
with open(master_dir+'/phonopy_params.conf','r') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    dimensions = lines[1].split('=')[1]

for dir in os.listdir(phonopy_dir):
    print('Working in directory: '+dir)
    os.chdir(phonopy_dir+dir)

    #generate displacements
    os.system("phonopy --dim=\'"+dimensions+"\' -d -c POSCAR-unit")

#============== began from init_vasp.py
    # find all supercell files
    supcell_filename_list = [n for n in os.listdir()\
        if re.fullmatch(pattern='POSCAR-\d{3}', string=n) is not None]

    for supcell_filename in supcell_filename_list:
        # make folder
        index = supcell_filename.split('-')[1]
        supcell_folderpath = 'supcell_{}'.format(index)
        os.makedirs(supcell_folderpath, exist_ok=True)

        # copy POSCAR file
        dst = os.path.join(supcell_folderpath, 'POSCAR')
        shutil.copyfile(supcell_filename, dst)
        
        #copy INCAR-ff file
        dst = os.path.join(supcell_folderpath, 'INCAR')
        shutil.copyfile(os.getcwd()+'/INCAR-ff',dst)

        # copy misc cells
        for misc_filename in misc_filename_list:
            dst = os.path.join(supcell_folderpath, misc_filename)
            shutil.copyfile(misc_filename, dst)
#==============

        # copy bat_vasp file
        dst = os.path.join(supcell_folderpath, 'bat1_vasp')
        shutil.copyfile(master_dir+'/bat1_vasp',dst)
            
        #copy params.conf file
        dst = os.path.join(supcell_folderpath, 'params.conf')
        shutil.copyfile(master_dir+'/params.conf', dst)

        #execute bat_vasp
        material_dir = os.getcwd()
        os.chdir(os.getcwd()+'/'+supcell_folderpath)
        os.system('sbatch --job-name=forces-vasp bat1_vasp')
        os.system('sleep 1') #give scheduler a break
        os.chdir(material_dir)
