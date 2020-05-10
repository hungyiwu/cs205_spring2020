import sys
import postprocessing_spark as pps

if __name__ == '__main__':
    directory = sys.argv[1]
    bands = pps.band_structure_collection(directory)
    indirect_band_gap = pps.indirect_band_gap(bands, 0.01)
    print(indirect_band_gap)

