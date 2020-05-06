import vasp_config as vc 
import re
import os
from shutil import copyfile
import phonopy_config_generator as pcg

vasp_dir_new = '/vasp_relax/'
phonopy_inputs_dir = '/phonopy_inputs/'
os.makedirs(os.getcwd()+phonopy_inputs_dir, exist_ok = True)

master_dir = os.getcwd()

for dir in os.listdir(os.getcwd()+vasp_dir_new):
    if not re.match('config',dir):
        print("Working in directory: " + dir)
        
        os.chdir(os.getcwd()+vasp_dir_new+dir)
        os.makedirs(master_dir+phonopy_inputs_dir+dir, exist_ok = True)

        v = vc.Vasp_Config(os.getcwd()+'/config')
        incar_params = v.params
        incar_params["NSW"]=1

        v.INCAR_writer(incar_params,fname="/../.."+phonopy_inputs_dir+dir+'/INCAR-ff')
        copyfile("CONTCAR", master_dir+phonopy_inputs_dir+dir+"/POSCAR-unit")
        v.relax_off(master_dir+phonopy_inputs_dir+dir+"/POSCAR-unit") # turn off selective dynamics
        
        #create band.conf and mesh.conf for phonopy input
        p = pcg.PhonopyConfig(config_f=os.getcwd()+"/config",params_f=master_dir+'/phonopy_params.conf')
        p.phonopy_config_writer(band=master_dir+phonopy_inputs_dir+dir+'/band.conf',mesh=master_dir+phonopy_inputs_dir+dir+'/mesh.conf')
        os.chdir(master_dir)
