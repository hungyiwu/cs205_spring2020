import os
import sys
import shutil
import re

#change to proper directory
phonopy_dir = '/n/holyscratch01/cs205/group4/mwenny/example/'

master_dir = os.getcwd()
output_dir = sys.argv[1] #pass desired output to script
os.makedirs(output_dir, exist_ok=True)

for dir in os.listdir(phonopy_dir):
    print('Working in directory: '+dir)
    os.chdir(phonopy_dir+dir)
    
    #make output directory for each material
    #os.makedirs(output_dir+dir, exist_ok=True)

    #parse VASP output and make force field file
    supcell_filename_list = [n for n in os.listdir()\
            if re.match(pattern='supcell_', string = n) is not None]

    '''
    for supcell in supcell_filename_list:
        if os.path.isfile(os.getcwd()+'/'+supcell+'/vasprun.xml')==False:
            os.system('mv '+os.getcwd()+' '+ phonopy_dir+'../vasp_run/')
            break
    '''
    os.system('phonopy -f ./supcell_{001..'+str(len(supcell_filename_list))+'}/vasprun.xml -c POSCAR-unit')

    #band structure
    os.system('phonopy -p band.conf -c POSCAR-unit -v')

    #density of states
    os.system('phonopy -p mesh.conf -c POSCAR-unit -v')

    #copy files over to output
    shutil.copyfile(os.getcwd()+'/band.hdf5', output_dir+'band_'+dir+'.hdf5')
    #shutil.copyfile(os.getcwd()+'/mesh.hdf5', output_dir+'mesh_'+dir+'.hdf5')
    shutil.copyfile(os.getcwd()+'/total_dos.dat', output_dir+'total_dos_'+dir+'.dat')
