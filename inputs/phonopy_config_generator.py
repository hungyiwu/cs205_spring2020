#author Malia Wenny
#mwenny@g.harvard.edu

import os

class PhonopyConfig(object):

    def __init__(self, config_f=None, params_f=None):
        if config_f is None:
            self.config = './config'
        else:
            self.config = config_f

        if params_f is None:
            self.params = './phonopy_params.conf'
        else:
            self.params = params_f

        self.nlayers = 0
        self.ATOM_NAME = 'ATOM_NAME='
        self.DIM = ''
        self.BAND = ''
        self.BAND_POINTS = ''
        self.MP = ''

        #============================
        #this section written with heavy guidance from vasp_config.py
        with open(self.config, 'r') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
            self.nlayers = (len(lines))/5

            atomlist = []
            for l in range(int(self.nlayers)):
                ibeg = l*5
                iend = ibeg+5
                thislayer = lines[ibeg:iend]

                atomlist.append(thislayer[0].split(' '))

        #===========================

        atomlist = [atoms for sublist in atomlist for atoms in sublist] #flatten
        for atom in atomlist:
            self.ATOM_NAME += atom + ' '

        with open(self.params, 'r') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
            self.DIM = lines[1]
            self.BAND = lines[2]
            self.BAND_POINTS = lines[3]
            self.MP = lines[4]

    def phonopy_config_writer(self, band='band.conf',mesh='mesh.conf'):

        #write band.conf
        with open(band,'w') as f:
            f.write('EIGENVECTORS = .TRUE.\n'+self.DIM+'\n'+self.ATOM_NAME+'\n'+self.BAND+'\n'+self.BAND_POINTS+'\n'+'BAND_LABELS=\Gamma M K \Gamma'+'\nHDF5=.TRUE.')

        with open(mesh,'w') as f:
            f.write(self.DIM+'\n'+self.ATOM_NAME+'\n'+self.MP+'\nHDF5=.TRUE.')


