import sys
import os
import shutil

if __name__ == '__main__':
    logscale = sys.argv[1]
    dirpath = './fake_1e{}'.format(logscale)
    srcpath = 'band_WSe2.hdf5'
    num_files = int(10**int(logscale))

    os.mkdir(dirpath)
    for i in range(num_files):
        dstpath = os.path.join(dirpath, 'band_{}.hdf5'.format(i))
        shutil.copyfile(srcpath, dstpath)
