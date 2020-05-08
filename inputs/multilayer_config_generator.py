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
            self.multilayer_directory = "./multilayer_TMDC_config/" #default multilayer directory
        else:
            self.multilayer_directory = multilayer_directory
        if alignments is None:
            self.alignments = np.array([0, 0, 0, 0, 0]) #default zero angle alignment
        else:
            self.alignments = np.array(alignments)
        if verticals is None:
            self.verticals = np.array([6.24, 6.24, 6.24, 6.24, 6.24]) #default 5 unit vertical
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
        self.fname = []
        os.makedirs(self.multilayer_directory, exist_ok=True)
        for number in self.layer_number:
            stacks = list(it.product(range(self.poscar_number), repeat=number))
            for stack in stacks:
                temp_transition_metal = self.transition_metal[list(stack)]
                temp_chalcogen = self.chalcogen[list(stack)]
                filename = "config_" + ''.join(temp_transition_metal) + "_" + ''.join(temp_chalcogen) + "_alignments__" + np.array2string(self.alignments[0:number], separator="_")[1:-1].replace(" ","") + "_verticals__" + np.array2string(self.verticals[0:number], separator="_")[1:-1].replace(" ", "")
                f = open(self.multilayer_directory+filename, "w")
                self.fname.append(filename)
                for iii in range(number):
                    f.write(temp_transition_metal[iii] + " " + temp_chalcogen[iii] + "\n1 2\n")
                    f.write(str(self.alignments[iii]) + "\n" + str(self.verticals[iii]) + "\n\n")
                f.close()

class RelaxedBilayerMultilayerSet(object):

    def __init__(self, relaxed_bilayers, layer_number=None, multilayer_directory=None):
        self.relaxed_bilayers = relaxed_bilayers
        if layer_number is None:
            self.layer_number = [3, 4, 5] #default to 3-5 multilayers
        else:
            self.layer_number = layer_number
        if multilayer_directory is None:
            self.multilayer_directory = "./relaxed_bilayer_multilayer_TMDC_config/" #default multilayer directory
        else:
            self.multilayer_directory = multilayer_directory

        # make list of TMDC relaxed bilayer species and optimized distances/alignments
        self.transition_metal = []
        self.chalcogen = []
        self.alignment = []
        self.vertical = []
        f = open(self.relaxed_bilayers)
        for line in f:
            line = line.split("_")
            temp = re.findall('[A-Z][^A-Z]*', line[1])
            self.transition_metal.append((temp[0], temp[1]))
            temp = re.findall('[A-Z][^A-Z]*', line[2])
            self.chalcogen.append((temp[0], temp[1]))
            self.alignment.append((line[5],line[6]))
            self.vertical.append((line[9],line[10].split(',')[1]))


        # make lists of trilayer TMDCS        
        self.multilayer_transition_metal = []
        self.multilayer_chalcogen = []
        self.multilayer_alignment = []
        self.multilayer_vertical = []
        for iii in range(len(self.transition_metal)):
            for jjj in range(len(self.transition_metal)):
                if (self.transition_metal[iii][1]==self.transition_metal[jjj][0]) and (self.chalcogen[iii][1]==self.chalcogen[jjj][0]) and (self.alignment[iii][1]==self.alignment[jjj][0]):
                    self.multilayer_transition_metal.append((self.transition_metal[iii][0], self.transition_metal[iii][1], self.transition_metal[jjj][1]))
                    self.multilayer_chalcogen.append((self.chalcogen[iii][0], self.chalcogen[iii][1], self.chalcogen[jjj][1]))
                    self.multilayer_alignment.append((self.alignment[iii][0], self.alignment[iii][1], self.alignment[jjj][1]))
                    self.multilayer_vertical.append((self.vertical[iii][0], self.vertical[iii][1], str(float(self.vertical[iii][1]) + float(self.vertical[jjj][1]))))


    def config_writer(self):
        os.makedirs(self.multilayer_directory, exist_ok=True)
        for iii in range(len(self.transition_metal)):
            filename = "config_" + ''.join(self.multilayer_transition_metal[iii]) + "_" + ''.join(self.multilayer_chalcogen[iii]) + "_alignments__" + '_'.join(self.multilayer_alignment[iii]) + "_verticals__" + '_'.join(self.multilayer_vertical[iii])
            f = open(self.multilayer_directory+filename, "w")
            for jjj in range(3):
                f.write(self.multilayer_transition_metal[iii][jjj] + " " + self.multilayer_chalcogen[iii][jjj] + "\n1 2\n")
                f.write(str(self.multilayer_alignment[iii][jjj]) + "\n" + str(self.multilayer_vertical[iii][jjj]) + "\n\n")
            f.close()
