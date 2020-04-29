import matplotlib.pyplot as plt
import postprocessing_spark as pps

bands = pps.band_structure_collection('.')
indirect_band_gap = pps.indirect_band_gap(bands, 0.01)
print(indirect_band_gap)

dos = pps.dos_collection('.')
print(pps.max_material_dos(dos).collect())
print(pps.max_dos(dos))
