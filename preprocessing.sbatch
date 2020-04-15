#!/bin/bash
#SBATCH --job-name=prep
#SBATCH -n 1 # Number of cores requested
#SBATCH -t 0:00:10 # Runtime in minutes
#SBATCH -p shared,test # Partition to submit to
#SBATCH --mem-per-cpu=8G # Memory per cpu in MB (see also--mem)
#SBATCH -o job_%j.out # Standard out goes to this file
#SBATCH -e job_%j.err # Standard err goes to this file
#SBATCH --account=cs205

# paths and parameters
UNITCELL_FILEPATH="./POSCAR_Gr"
VASP_FILEPATH="vasp.std"
CONDAENV_NAME="cs205"
DIM_X=2
DIM_Y=3

# load environment
source activate $CONDAENV_NAME

# pre-processing
phonopy --dim="$DIM_X $DIM_Y 1" -d -c $UNITCELL_FILEPATH

# initiate vasp jobs
python init_vasp.py $VASP_FILEPATH
