import postprocessing as pp
import matplotlib.pyplot as plt

test_BS = pp.BandStructure('band_WSe2.hdf5')

plt.figure()
plt.plot(test_BS.distance, test_BS.frequency)
plt.show()


test_DOS = pp.DensityOfStates('total_dos.dat')

plt.figure()
plt.plot(test_DOS.frequency, test_DOS.dos)
plt.show()
