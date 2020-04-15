#!/bin/bash
#SBATCH --job-name=postp
#SBATCH -n 1 # Number of cores requested
#SBATCH -t 0:00:10 # Runtime in minutes
#SBATCH -p shared,test # Partition to submit to
#SBATCH --mem-per-cpu=8G # Memory per cpu in MB (see also--mem)
#SBATCH -o job_%j.out # Standard out goes to this file
#SBATCH -e job_%j.err # Standard err goes to this file
#SBATCH --account=cs205

# paths and parameters
UNITCELL_FILEPATH="./POSCAR_Gr"
BANDCONF_FILEPATH="./band.conf"
MESHCONF_FILEPATH="./mesh.conf"
CONDAENV_NAME="cs205"

# load modules
module load python hdf5
source activate $CONDAENV_NAME

# post-processing: 
# generate force-field
phonopy -f ./*/vasprun.xml -c $UNITCELL_FILEPATH
# plot band structure
phonopy -p -s $BANDCONF_FILEPATH -c $UNITCELL_FILEPATH
# plot density of states
phonopy -p -s $MESHCONF_FILEPATH -c $UNITCELL_FILEPATH
