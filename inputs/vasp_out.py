import vasp_config as vc
import multilayer_config_generator as mcg
from pymatgen.io.vasp import outputs
import sys
import os
import re
from shutil import copyfile
import matplotlib.pyplot as plt
import numpy as np

vasp_dir = "/vasp_relax_test/" # master directory to run vasp
E0 = [] # the list of energies

# generate input files for 10 different layer separations
for dz in range(20):
    # create config file
    set = mcg.MultilayerSet(layer_number=[2], alignments=[0,180], verticals=[0,5.5+0.05*dz])
    set.config_writer()
    
    fname = set.fname
    
    for f in fname:
        folder = f[7:]
        subdir = vasp_dir+folder

        if re.match("config_WW_SeSe",f):
            masterdir = os.getcwd()
            os.chdir(os.getcwd()+subdir)
            outcar = outputs.Outcar("OUTCAR")
            E0.append(outcar.final_energy)
            os.chdir(masterdir)
            
print(E0-np.min(E0))
