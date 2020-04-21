# author Taylor Lee Patti
# taylorpatti@g.harvard.edu

import os
import re
import numpy as np
import itertools as it

class MultilayerSet(object):

    def __init__(self, layer_number=None, monolayer_directory=None, multilayer_directory=None, alignments=None, verticals=None):
        if layer_number is None:
            self.layer_number = [1, 2, 3, 4, 5] #default to 1-5 multilayers
        else:
            self.layer_number = layer_number
        if monolayer_directory is None:
            self.monolayer_directory = "./TMDC_poscar/" #default monolayer directory
        else:
            self.monolayer_directory = monolayer_directory
        if multilayer_directory is None:
            self.multilayer_directory = "./multilayer_TMDC_poscar/" #default multilayer directory
        else:
            self.multilayer_directory = multilayer_directory
        if alignments is None:
            self.alignments = np.array([0, 0, 0, 0, 0]) #default zero angle alignment
        else:
            self.alignments = np.array(alignments)
        if verticals is None:
            self.verticals = np.array([5, 5, 5, 5, 5]) #default 5 unit vertical
        else:
            self.verticals = np.array(verticals)


        # make list of TMDC monolayer transition metals and chalcogens
        monolayer_poscars = os.listdir(self.monolayer_directory)
        self.poscar_number = len(monolayer_poscars)
        self.transition_metal = []
        self.chalcogen = []
        for monolayer in monolayer_poscars:
            monolayer = monolayer.split("_")[1]
            monolayer = re.findall('[A-Z][^A-Z]*', monolayer)
            monolayer[1] = monolayer[1][:-1]
            self.transition_metal.append(monolayer[0])
            self.chalcogen.append(monolayer[1])
        self.transition_metal = np.array(self.transition_metal)
        self.chalcogen = np.array(self.chalcogen)

    def config_writer(self):
        #make configuration file for each stack size and permutation with repititions
        os.makedirs(self.multilayer_directory, exist_ok=True)
        for number in self.layer_number:
            stacks = list(it.product(range(self.poscar_number), repeat=number))
            for stack in stacks:
                temp_transition_metal = self.transition_metal[list(stack)]
                temp_chalcogen = self.chalcogen[list(stack)]
                filename = "config_" + ''.join(temp_transition_metal) + "_" + ''.join(temp_chalcogen) + "_alignments__" + np.array2string(self.alignments[0:number], separator="_")[1:-1].replace(" ","") + "_verticals__" + np.array2string(self.verticals[0:number], separator="_")[1:-1].replace(" ", "")
                f = open(self.multilayer_directory+filename, "w")
                for iii in range(number):
                    f.write(temp_transition_metal[iii] + " " + temp_chalcogen[iii] + "\n1 2\n")
                    f.write(str(self.alignments[iii]) + "\n" + str(self.verticals[iii]) + "\n\n")
                f.close()
