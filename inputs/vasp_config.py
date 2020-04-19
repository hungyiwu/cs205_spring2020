# author: ziyan zhu
# zzhu1@g.harvard.edu

import os
import numpy as np
from math import *
import re
import pymatgen.core.structure as struct
import pymatgen.io.vasp.inputs as inputs

class Vasp_Config(object):
    # Create the input file for layered TMDCs
    # Read from config:

    def __init__(self, target="config"):
        self.a0 = 0 # lattice constant
        self.zsep = 0 # chalcogen-metal separation
        self.alignment = 0 # 0 deg. or 180 deg. / (parallel or anti-parallel)
        self.mat = np.array([]) # list of elements
        self.nlayers = 1
        self.dz = [] # list of interlayer separations

        # default INCAR parameters for relaxation
        self.params = {
        "SYSTEM":"TMDC",
        "ISTART":0,
        "ISMEAR":0,
        "SIGMA":0.01,
        "ENCUT":800,
        "AMIN":0.01,
        "NSW":100, # change to 1 when calculating the force field
        "EDIFF":1E-8,
        "IBRION":-1,
        "SYMPREC":0.0001, # the precision of poscar
        "NPAR":1,
        "ADDGRID":".TRUE.", # determines whether an additional support grid is used for the evaluation of the augmentation charge
        "LREAL":".FALSE.",
        "LWAVE":".FALSE.", # write wave function
        "ALGO":"N",
        "NELMIN":5,
        "PREC":"Accurate",

        # vdw correction
        "METAGGA":"SCAN",
        "LASPH":"T",
        "LUSE_VDW":"T",
        "BPARAM":"15.7"
        }
        
        # read info from config
        with open(target, 'r') as f:
            thelines = f.readlines()
            thelines = [x.strip() for x in thelines]
            thelines = filter(lambda x: x != "", thelines)  # in py3, this is an object
            thelines = [x for x in thelines]
            nlayers = len(thelines)/4.0
            self.nlayers = int(nlayers)
            if nlayers != np.floor(nlayers):
                print("Check your input file!")
            else:
                print("There are " + str(int(nlayers)) + " layers.")
            
            # Read the POSCAR for each layer
            self.a0 = np.zeros([int(nlayers),1])
            self.zsep = np.zeros([int(nlayers),1])
            self.alignment = np.zeros([int(nlayers),1])
            self.dz = np.zeros([int(nlayers), 1])
            for l in range(int(nlayers)):
                ibeg = l*4
                iend = ibeg+4
                lines = thelines[ibeg:iend]
                
                # Read info from config
                mat = lines[0].split(" ")
                num = lines[1].split(" ")
                self.alignment[l] = int(lines[2])
                self.dz[l] = float(lines[3])
                
                # read POSCAR
                filepath = "./TMDC_poscar/"
            
                fname = "POSCAR_"
                for n in range(len(mat)):
                    fname = fname + mat[n]
                    if num[n] != "1":
                        fname = fname + num[n]
                    for m in range(int(num[n])):
                        self.mat = np.append(self.mat,mat[n])

                #try:
                poscar = struct.IStructure.from_file(filepath + fname)
                self.a0[l] = poscar.lattice.abc[0]
                z_pos = np.zeros([3,1])
                for a_idx in range(3): # assuming there are 3 atoms
                    z_pos[a_idx] = poscar.cart_coords[a_idx][2]
                    if z_pos[a_idx] > 0.5*poscar.lattice.c:
                        z_pos[a_idx] = z_pos[a_idx]-poscar.lattice.c
                        
                self.zsep[l] = (np.max(z_pos) - np.min(z_pos))/2
               
#                except:
#                    print("Structure file does not exist!")
    
    def POSCAR_writer(self,fname="POSCAR"):
        vac = 15 # vacuum spacing
        c = vac + np.sum(self.dz) + np.sum(self.zsep)
        a0 = np.mean(self.a0) # let the combined lattice constant be the averaged value
        A0 = [[1*a0, 0, 0],
            [-0.5*a0, sqrt(3)/2*a0, 0],
            [0, 0, c]]
        
        # create atomic positions for all layers in Cartesian coordinate
        coords = np.zeros([self.nlayers*3,3])
        z_here = 0
        for l in range(self.nlayers):
            z_here = z_here + self.dz[l]
            if l > 0:
                z_here = z_here + self.zsep[l]
                
            if self.alignment[l] == 0:
                coords_here = np.array([[0, 0, 0],
                    [1./3, 2./3, -self.zsep[l]],
                    [1./3, 2./3, self.zsep[l]]])
                
            else:
                coords_here = [[1./3, 2./3, 0],
                    [0, 0, -self.zsep[l]],
                    [0, 0, self.zsep[l]]]
                    
            coords[l*3:(l+1)*3][:] = coords_here
            coords[l*3:(l+1)*3,2] += z_here
            coords[l*3:(l+1)*3,2] = coords[l*3:(l+1)*3,2] / c
        
        # relax the atomic positions in the z direction
        relax = [[False, False, True] for x in range(self.nlayers*3)]
        relax[0][2]=False
        #print(relax)
                
        layers = struct.Structure(A0,self.mat,coords,coords_are_cartesian=False)
        out = inputs.Poscar(layers)
        out.selective_dynamics=relax
        out.write_file(os.getcwd()+fname)
        
    
    def POTCAR_writer(self):

        # Create POTCAR
        catstring = 'cat '
        cwd = os.getcwd()
        
#        # find the list of non-repeating elements
#        previous = None
#        mat = ""
#        for x in mat_all:
#            if x != previous:
#                mat = mat + x + "\t"
#            previous = x
#        mat = np.sort(mat.split("\t"))
#        #print(mat)
        
        
        for name in self.mat:
            if name != "":
                catstring+= os.getcwd() + '/PPs/' + name + '_POTCAR '
        
        # print(catstring)

        catstring += "> POTCAR"

        try:
            os.system(catstring)
        except:
            print('POTCAR not found!')

    def INCAR_writer(self,params,fname="/INCAR"):
        incar = inputs.Incar(params)
        incar.write_file(os.getcwd()+fname)

    def KPOINT_writer(self,fname="/KPOINTS"):
        nk = [[13, 13, 1]]
        kpt = inputs.Kpoints(comment='k grid', kpts=nk, kpts_shift=(0,0,0))
        kpt.write_file(os.getcwd()+fname)

    def vasp_run(self, vaspdir = "./vasp.std"):
        os.system('mpirun -n $SLURM_NTASKS ' + vaspdir )

if __name__ == '__main__':
    pass
