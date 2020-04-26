import vasp_config as vc
import multilayer_config_generator as mcg
import sys
import os
import re
from shutil import copyfile
import time

vasp_dir = "/vasp_relax_test/" # master directory to run vasp

# generate input files for 10 different layer separations
for dz in range(20):
    # create config file
    set = mcg.MultilayerSet(layer_number=[2], alignments=[0,180], verticals=[0,3.8+0.07*dz])
    set.config_writer()
    dir = set.multilayer_directory[1:]
    print(dir)
    fname = set.fname
    
    for f in fname:
        folder=f[7:]
        # os.system("cd " + vasp_dir)
        os.makedirs(os.getcwd()+vasp_dir+folder, exist_ok = True)
        copyfile(os.getcwd()+dir+f,os.getcwd()+vasp_dir+folder+"/config")
        
        subdir = vasp_dir+folder
        # print(subdir)
        v = vc.Vasp_Config(target=os.getcwd()+subdir+"/config")
    
        v.POSCAR_writer(subdir+"/POSCAR")
        v.POTCAR_writer(subdir+"/POTCAR",subdir+"/POSCAR")
        v.KPOINT_writer(subdir+"/KPOINTS")
        params = v.params
        params["ISIF"]=3
        params["NPAR"]=2
        params["NSW"]=2
        v.INCAR_writer(v.params,subdir + "/INCAR")
        
        #if re.match("config_WW_SeSe",f):
        print(subdir)
        masterdir = os.getcwd()
        print(masterdir)
        os.chdir(os.getcwd()+subdir)
        copyfile(masterdir + '/bat_vasp', os.getcwd()+'/bat_vasp')
        copyfile(masterdir + '/params.conf', os.getcwd()+'/params.conf')
        os.system('sbatch bat_vasp')
        os.chdir(masterdir)
