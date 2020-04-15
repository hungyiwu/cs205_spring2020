# Automated pipeline for pre-, force-field, and post-processing

1. Edit ```params.conf``` as needed

   Configuration file for sbatch scripts (```preprocessing.sbatch``` and ```postprocessing.sbatch```).

2. Run pre-processing

   ```sbatch preprocessing.sbatch```. This runs ```phonopy``` and generates super-cells with different displacements,  
   makes folder structures for each super-cell, writes sbatch scripts for VASP calculations, and then generates  
   one master bash script to kick-off all jobs with proper job dependencies.

   Except for the initial ```phonopy``` calls, all other tasks will be done through the Python script ```init_vasp.py```  
   called by ```preprocessing.sbatch```.

   Post-processing, ```postprocessing.sbatch```, will be initiated after all  VASP calculations of this material  
   are finished without error.

### Note:

   Maximum number of jobs allowed to run simultaneously seems to be only supported in array jobs only  
   (see <https://slurm.schedmd.com/sbatch.html>).
> A maximum number of simultaneously running tasks from the job array may be specified using a "%" separator.  
> For example "--array=0-15%4" will limit the number of simultaneously running tasks from this job array to 4.
