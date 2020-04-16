# ziyan zhu
# zzhu1@g.harvard.edu

import numpy as np

import pymatgen.core.structure as struct
import pymatgen.io.vasp.inputs as inputs

with open('config', 'r') as f:
    thelines = f.readlines()
    thelines = [x.strip() for x in thelines]
    thelines = filter(lambda x: x != "", thelines)
    nlayers = len(thelines)/3.0
    if nlayers != np.floor(nlayers):
        print("Check your input file!")
    else:
        print("There are " + str(int(nlayers)) + " layers.")
        
    for l in range(int(nlayers)):
        ibeg = l*3
        iend = ibeg+3
        lines = thelines[ibeg:iend]
        
        # read POSCAR from the query folder
        filepath = "../query/TMDC_poscar/"
        mat = lines[0].split(" ")
        num = lines[1].split(" ")
        fname = "POSCAR_"
        for n in range(len(mat)):
            fname = fname + mat[n]
            if num[n] != "1":
                fname = fname + num[n]
        
        try:
            poscar = struct.IStructure.from_file(filepath + fname)
            print(poscar.cart_coords)
        except:
            print("Structure file does not exist!")
        
