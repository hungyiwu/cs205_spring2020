import os
import pyspark
from pyspark import SparkConf, SparkContext
import glob
import h5py
import numpy as np

def band_structure_collection(directory):
    #load all band structure files in directory and organize them in an RDD labeled with filename
    sc = SparkContext(appName='SparkHDF5')
    filenames = glob.glob(os.path.join(directory, 'band*'))
    filenames = sc.parallelize(filenames)
    files = filenames.map(lambda filename: (filename, band_structure(filename))) #creates (filename, (distance_array, frequency_matrix))
    return files

def dos_collection(directory):
    #load all dos structure files in directory and organize them in an RDD labeled with filename
    sc = SparkContext(appName='SparkHDF5')
    filenames = glob.glob('total*')
    filenames = sc.parallelize(filenames)
    files = filenames.map(lambda filename: (filename, dos(filename))) #creates (filename, (frequency_array, dos_array))
    return files

def band_structure(filename):
    #load individual band structures and return arrays of k and frequency
    f = h5py.File(filename, 'r')
    distance = f['distance']
    distance = np.reshape(distance, (distance.shape[0]*distance.shape[1])) #reshape into (k_index, frequency)
    frequency = f['frequency']
    frequency = np.reshape(frequency, (frequency.shape[0]*frequency.shape[1], frequency.shape[2])) #reshape into (k_index, frequency, band_number)
    return distance, frequency

def dos(filename):
    #load individual dos files and return arrays of frequency and dos
    f = open(filename)
    frequency = []
    dos = []
    f.readline() #skip first line, contains metadata
    for line in f:
        line = line.split()
        frequency.append(float(line[0]))
        dos.append(float(line[1]))
    return np.array(frequency), np.array(dos)

def indirect_band_gap(rdd, tolerance):
    #compute indirect band gap for band_structure_collection
    #specify that band gaps are greater than small constant tolerance>0
    rdd_max = max_freq_in_material(rdd).sortByKey().collect() #sort keys (materials) in case material order different
    rdd_min = min_freq_in_material(rdd).sortByKey().collect()
    band_gaps = []
    for material in range(len(rdd_max)):
        temp = rdd_min[material][1][1][1:6] - rdd_max[material][1][1][0:5]
        band_gaps.append((rdd_max[material][0], temp[temp > tolerance]))
    #returns list of tuples (filename, array_of_indirect_band_gaps) where latter is possibly empty
    return band_gaps

def max_freq_in_material(rdd):
    #returns (filename, (distance_points_array, max_frequency_array))
    #where max_frequency_array is the highest frequency of each band
    #and distance_points_array are the corresponding distance values
    return rdd.map(lambda structure: (structure[0], (structure[1][0][np.argmax(structure[1][1], axis=0)], np.max(structure[1][1], axis=0))))

def min_freq_in_material(rdd):
    #returns (filename, (distance_points_array, min_frequency_array))
    #where min_frequency_array is the lowest frequency of each band
    #and distance_points_array are the corresponding distance values
    return rdd.map(lambda structure: (structure[0], (structure[1][0][np.argmin(structure[1][1], axis=0)], np.min(structure[1][1], axis=0))))

def max_dos(rdd):
    rdd_max = max_material_dos(rdd)
    #returns tuple (filename, (frequency, max_dos))
    #for a single filename that has greatest max_dos
    return rdd_max.max(lambda structure: structure[1][1])

def max_material_dos(rdd):
    #returns rdd with tuples (filename, (frequency, max_dos))
    #where max_dos is the max dos for each material in filename
    #and frequency is the corresponding frequency
    return rdd.map(lambda structure: (structure[0], (structure[1][0][np.argmax(structure[1][1])], np.max(structure[1][1]))))
