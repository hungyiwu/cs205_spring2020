import vasp_config as vc
import os
from shutil import copyfile
import phonopy_config_generator as pcg

#change thiis to proper directory
vasp_dir_new = '/n/holyscratch01/cs205/group4/zzhu/example/'

#change to desired output directory
phonopy_inputs_dir = '/n/holyscratch01/cs205/group4/mwenny/example/'

os.makedirs(phonopy_inputs_dir, exist_ok = True)
temp_dir = '/temp_dir/'
os.makedirs(os.getcwd()+temp_dir, exist_ok=True)

master_dir = os.getcwd()

for dir in os.listdir(vasp_dir_new):
    print("Working on directory: " + dir)

    os.makedirs(phonopy_inputs_dir+dir, exist_ok = True)
    os.makedirs(master_dir+temp_dir+dir, exist_ok=True)
    #print('Sending to: '+master_dir+phonopy_inputs_dir+dir)

    #pass fake config, don't actually need it but need to give something to function
    v = vc.Vasp_Config(master_dir+'/config')
    
    #incar
    incar_params = v.params
    incar_params["NPAR"] = 4
    incar_params["NSW"]=1
    v.INCAR_writer(incar_params,fname=temp_dir+dir+'/INCAR-ff')
    copyfile(master_dir+temp_dir+dir+'/INCAR-ff', phonopy_inputs_dir+dir+'/INCAR-ff')

    #poscar
    copyfile(vasp_dir_new+dir+"/POSCAR-unit", master_dir+temp_dir+dir+"/POSCAR-unit")
    v.relax_off(master_dir+temp_dir+dir+"/POSCAR-unit") # turn off selective dynamics
    copyfile(master_dir+temp_dir+dir+'/POSCAR-unit', phonopy_inputs_dir+dir+'/POSCAR-unit')

    #potcar
    v.POTCAR_writer(temp_dir+dir+"/POTCAR",poscar_dir=temp_dir+dir+"/POSCAR-unit")
    copyfile(master_dir+temp_dir+dir+'/POTCAR', phonopy_inputs_dir+dir+'/POTCAR')

    #kpoints
    v.KPOINT_writer(temp_dir+dir+"/KPOINTS")
    copyfile(master_dir+temp_dir+dir+'/KPOINTS', phonopy_inputs_dir+dir+'/KPOINTS')

    #band.conf
    copyfile(vasp_dir_new+dir+"/band.conf", phonopy_inputs_dir+dir+"/band.conf")
    #copyfile(vasp_dir_new+dir+"/mesh.conf", master_dir+phonopy_inputs_dir+dir+"/mesh.conf")

os.system('rm -rf temp_dir')
