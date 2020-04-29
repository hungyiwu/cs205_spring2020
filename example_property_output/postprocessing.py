# author Taylor Lee Patti
# taylorpatti@g.harvard.edu

import h5py
import numpy as np
import matplotlib.pyplot as plt

class BandStructure(object):

    def __init__(self, filename):
        self.filename = filename

        f = h5py.File(filename, 'r')
        self.distance = f['distance']
        self.distance = np.reshape(self.distance, (self.distance.shape[0]*self.distance.shape[1])) #reshape into (k_index, frequency)
        self.frequency = f['frequency']
        self.frequency = np.reshape(self.frequency, (self.frequency.shape[0]*self.frequency.shape[1], self.frequency.shape[2])) #rehape into (k_index, frequency, band_number)


class DensityOfStates(object):

    def __init__(self, filename):
        self.filename = filename
        f = open(self.filename)

        self.frequency = []
        self.dos = []
        f.readline() #skip first line, contains metadata
        for line in f:
            line = line.split()
            self.frequency.append(float(line[0]))
            self.dos.append(float(line[1]))
        self.frequency = np.array(self.frequency)
        self.dos = np.array(self.dos)

