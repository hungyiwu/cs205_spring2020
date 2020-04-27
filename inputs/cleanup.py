import vasp_config as vc 
import os
from shutil import copyfile

vasp_dir_new = '/vasp_relax/'
phonopy_inputs_dir = '/phonopy_inputs/'
os.makedirs(os.getcwd()+phonopy_inputs_dir, exist_ok = True)

master_dir = os.getcwd()

for dir in os.listdir(os.getcwd()+vasp_dir_new):
    print("Working in directory: " + dir)
    
    os.chdir(os.getcwd()+vasp_dir_new+dir)
    os.makedirs(master_dir+phonopy_inputs_dir+dir, exist_ok = True)

    v = vc.Vasp_Config(os.getcwd()+'/config')
    incar_params = v.params
    incar_params["NSW"]=1

    v.INCAR_writer(incar_params,fname="/../.."+phonopy_inputs_dir+dir+'/INCAR-ff')
    copyfile("CONTCAR", master_dir+phonopy_inputs_dir+dir+"/POSCAR-unit")
    v.relax_off(master_dir+phonopy_inputs_dir+dir+"/POSCAR-unit") # turn off selective dynamics
    
