# ziyan zhu
# zzhu1@g.harvard.edu
# read vasp output, fit energy vs. z to a parabolic fn, find the minimum energy
import vasp_config as vc
import multilayer_config_generator as mcg
from pymatgen.io.vasp import outputs
import sys
import os
import re
from shutil import copyfile
import matplotlib.pyplot as plt
import numpy as np

vasp_dir = "/vasp_relax_test/" # master directory for the previous run
vasp_dir_new = "/vasp_relax/" # new directory to run vasp at the optimal z 
nz = 20
E0 = [] # the list of energies
z = np.zeros([nz])
align = [0, 180]

# read from vasp runs 
for dz in range(nz):
    z[dz] = 3.8+0.07*dz
    # create config file
    set = mcg.MultilayerSet(layer_number=[2], alignments=align, verticals=[0,3.7+0.05*dz])
    set.config_writer()
    
    fname = set.fname
    
    for f in fname:
        folder = f[7:]
        subdir = vasp_dir+folder

        masterdir = os.getcwd()
        os.chdir(os.getcwd()+subdir)
        outcar = outputs.Outcar("OUTCAR")
        E0.append(outcar.final_energy)
        os.chdir(masterdir)
            
E_list = E0-np.min(E0)
p = np.polyfit(z, E_list,2)
zmin = -p[1]/(2*p[0])
print(zmin)

# submit another vasp run
# create config file
set = mcg.MultilayerSet(layer_number=[2], alignments=align, verticals=[0,zmin])
set.config_writer()
dir = set.multilayer_directory[1:]
print(dir)
fname = set.fname

for f in fname:
    folder=f[7:]
    # os.system("cd " + vasp_dir)
    os.makedirs(os.getcwd()+vasp_dir_new+folder, exist_ok = True)
    copyfile(os.getcwd()+dir+f,os.getcwd()+vasp_dir_new+folder+"/config")
    
    subdir = vasp_dir_new+folder
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
