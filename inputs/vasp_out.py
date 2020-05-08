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
from scipy.optimize import curve_fit

vasp_dir = "/vasp_relax_test/" # master directory for the previous run
vasp_dir_new = "/vasp_relax/" # new directory to run vasp at the optimal z 
#vasp_dir = "relaxed_bilayer_multilayer_TMDC_config" # master directory for the previous run
#vasp_dir_new = "/vasp_relax_trilayer/" # new directory to run vasp at the optimal z 
nz = 15
z = np.zeros([nz])
align = []
for arg in sys.argv[1:]:
    align.append(int(arg))
fname_all = np.array([])
f2 = open("zElist.txt", "a+")

# read from vasp runs and create a list of all subdirectories
for dz in range(nz):
    z[dz] = 3.6+0.14*dz
    # create config file
    set = mcg.MultilayerSet(layer_number=[2], alignments=align, verticals=[0,3.6+0.14*dz])
    set.config_writer()
    
    fname = set.fname
    fname_all = np.append(fname_all,fname)

# sort by filename
fname_all = np.sort(fname_all)
fname_all = [f[7:] for f in fname_all]
# unique materials combinations
fname = np.sort(fname)
fname = [f[7:] for f in fname]
    
# go through the unique materials combination and do a fit
# fit vdw 6-12 potential 
def func(x, a, b, c):
    return a*(-2/((b/x)**6) + 1/((b/x)**12)) + c

masterdir = os.getcwd()
z_list = []
for f_master in fname:
    E0 = [] # the list of energies
    m = re.search('verticals',f_master)
    iend = m.span()[0]
    pattern = f_master[0:iend]
    for f in fname_all:
        subdir = vasp_dir+f
        if f[0:len(pattern)] == pattern:
    
            os.chdir(os.getcwd()+subdir)
            print(os.getcwd())
            if os.path.exists("OUTCAR"):
                outcar = outputs.Outcar("OUTCAR")
                if outcar.final_energy is not None:
                    E0.append(outcar.final_energy)
            os.chdir(masterdir)
    
    if len(E0)==nz: # if the run is finished
        print(E0)
        E_list = E0-np.min(E0)
        #ind = np.argmin(E0)
        #zmin_tmp = z[ind]
        # popt,pcov = curve_fit(func,z,E_list,bounds=([0,zmin_tmp-0.07,0],[0.05,zmin_tmp+0.07,1]),p0=(0.01,zmin_tmp,0))
        zarr=np.linspace(np.min(z),np.max(z),500)
        p=np.polyfit(z,E_list,10)
        print(p)
        fit=np.poly1d(p)
        earr=fit(zarr)
        ind=np.argmin(earr)
        zmin=zarr[ind]
        z_list.append(zmin)
        print(zmin)
        for iii in range(len(z)):
            f2.write(pattern+","+str(z[iii])+","+str(E0[iii])+"\n")

        # submit another vasp run
        # create config file
        #set = mcg.MultilayerSet(layer_number=[2], alignments=align, verticals=[0,zmin])
        #set.config_writer()
        #dir = set.multilayer_directory[1:]
        #print(dir)
        #fname = np.sort(set.fname)

        #for f in fname:
        #    folder=f[7:]
        #    if folder[0:len(pattern)] == pattern:
        #        
        #        if os.path.exists(os.getcwd()+vasp_dir_new+folder+'/CONTCAR'):
        #            print("VASP run already done. Skip")
        #        else:
        #            os.makedirs(os.getcwd()+vasp_dir_new+folder, exist_ok = True)
        #            copyfile(os.getcwd()+dir+f,os.getcwd()+vasp_dir_new+folder+"/config")

        #            subdir = vasp_dir_new+folder
        #            # print(subdir)
        #            v = vc.Vasp_Config(target=os.getcwd()+subdir+"/config")

        #            v.POSCAR_writer(subdir+"/POSCAR")
        #            v.POTCAR_writer(subdir+"/POTCAR",subdir+"/POSCAR")
        #            v.KPOINT_writer(subdir+"/KPOINTS")
        #            params = v.params
        #            params["ISIF"]=3
        #            params["NPAR"]=2
        #            params["NSW"]=2
        #            v.INCAR_writer(v.params,subdir + "/INCAR")

        #            #print(subdir)
        #            masterdir = os.getcwd()
        #            #print(masterdir)
        #            os.chdir(os.getcwd()+subdir)
        #            copyfile(masterdir + '/bat_vasp', os.getcwd()+'/bat_vasp')
        #            copyfile(masterdir + '/params.conf', os.getcwd()+'/params.conf')
        #            os.system('sbatch bat_vasp')
        #            os.chdir(masterdir)

# write to file
f = open("zoptlist.txt", "a+")
for iii in range(len(fname)):
    f.write(fname[iii] + ',' + str(z_list[iii]) + '\n')
f.close()
f2.close()
