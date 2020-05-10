# Create VASP inputs files and combine monolayer TMDCs
## Before you start 
- Make a conda environment with `conda-env.yml`.
- Edit `params.config` to change the conda environment name 
- Make sure `vasp.std` is in this folder
- Confirm that Python package `pymatgen` is installed in the active environment.

## Relaxation
In this step, we sample 15 different interlayer spacings between bilayers (aligned/0-deg. or antialigned/180.deg) in order to find the optimal positions between each pair of layers. The outputs generated include: 

1. the list of optimal interlayer spacing `zoptlist.txt` 
2. ground state energy vs. interlayer spacing  `zElist.txt` 
3. Input parameters for phonopy calculations in folder `/phonopy_inputs`

### Running the workflow
To run the work flow, simply  do 

`sbatch zscan.batch`, which automatically runs 15 vasp calculations at different interlayer separations
After all relaxation calculations have finished, first extract the optimal interlayer separation and do a relaxation calculation at the optimal spacing, and copies the output structure and creates the INCAR for the force field calculation

05/04/2020 note: !!! Now relax.py and vasp_out.py takes alignment as the input. Need to change both `zscan.batch` and `vasp_out.batch`


## Analyzing the output data

To parse the output files and plot the results from `zElist.txt` and `zoptlist.txt`, run

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit zEanalysis_spark.py`. This will generates three figures and save to the `results` folder
<p float="left">
  <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_TeTe.png" width=400>
  <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/E0_TeTe.png" width=400>
</p>
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/E0_vs_z_TeTe.png" width=500>

This particular script groups the materials by chalcogens. We use Spark to organize the data. A speedup test using Spark dataframe is contained in the folder `/zEanalysis`. To run a speedup test, do 

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit select_zEdata.py <<metal>> <<chalcogen>> <<alignment>> <<np>>`.

which save the data that contains the given metal, chalcogen, with the given alignment (0 degree or 180 degrees), and <<np>> is the number of cores to use. For example, 

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit select_zEdata.py Mo S 0 4`

## Phonopy and VASP force field calculations

Given a set of relaxed multilayer structures, as created in the first step (which ends with `cleanup.batch`/`cleanup.py`), to run the phonopy and VASP force field calculations do:
1. Ensure that the directory containing the results from the first step is on the Cannon $SCRATCH directory (e.g. on `/n/holyscratch01/cs205/group4/<directory>`. This ensures that you don't fill up your home directory with large files.
2. Edit line 7 of `preprocess.py` to ensure that this script is reading the data from the correct directory. If desired, edit line 10 to change the force field directory (if you do, you must also change line 10 and line 7 in `forces_vasp.py` and `postprocess.py`, respectively). 
3. If desired, change `NPAR` in `preprocess.py` to run with different numbers of cores. If so, change `-n` in `bat1_vasp` to be `NPAR`^2. 

To run the entire workflow for this section, do: `sbatch preprocess.batch`. The results (in `.hdf5` format) will be written to the `$OUTPUTFILE_PATH` directory specified in `params.conf`.

## General Workflow
0. Create different config files using the MultilayerSet class in `multilayer_config_generator.py`
1. Combine different layers using the input in `config` and create VASP input files
2. Run VASP multiple calculations at different interlayer separation files that allows ions to move in the z-direction to find optimal interlayer separations 
3a. Fit the ground state energy vs. the interlayer separation as a function of z to a parabolic function. This also generates two datasets: input files for calculation, stored in folder `phonopy_inputs/` and output files contained in `zElist.txt` and `zoptlist.txt`. `zElist.txt` provides a list of materials, 15 interlayer separations and the corresponding ground state energies; `zoptlist.txt` contains a list of materials and the fitted optimal interlayer separation.
3b. Use the RelaxedBilayerMultilayerSet class to collect optimal vertical separations and alignments from the initial VASP calculation output files and obtain more precisely relaxed trilayers.
4. Perform a relaxation calculation at the optimal interlayer spearation. Copy the geometry to `/phonopy_inputs/' folder 
5. Copy the relaxed structure to `POSCAR-unit`, rewrite `INCAR-ff` for the force field calculation (same setting except for letting `NSW=1` for no ionic relaxation)
6. Generate phonopy supercells based on `POSCAR-unit` (number of supercells depends on symmetry/space group of structure).
7. Run a VASP force field calculation on each supercell.
8. Process the results using phonopy to generate `.hdf5` files containing band structure information.

Edit `config` file as needed 

#### Default  `config` file format: 
Each layer has four lines. 

Line 1: elements (order: metal, chalcogen)

Line 2: number of atoms corresponding to the element above 

Line 3: layer alignment with respect to the positive x axis (0 degree or 180 degrees, or equivalently, alignment or anti-alignment)

Line 4: Layer separation between this layer and the last layer. The separation is defined as the distance between the chalcogen atom of the layer ($\ell$-1) to the metal atom of the layer $\ell$

To construct config files, use the multilayer_config_generator.py file. Read class variables for specifics. See quickrunner.py for example run which combines TMDC_poscar monolayers into the multilayer permutations with repetition of up to 3 stacks in multilayer_TMDC_poscar.

To construct the structure, do

```python
import vasp_config as vc
v = vc.Vasp_Config(target='config')
```

To write `POSCAR`, `POTCAR`, `KPOINTS`, and `INCAR` do 
```python
v.POSCAR_writer()
v.POTCAR_writer()
v.KPOINTS_writer()
v.KPOINTS_writer(v.params)
```

Use and `params.config` from the phonopy pipeline to run initialize filepath, conda environment etc.

After the structure construction, perform a VASP calculation to allow out-of-plane relaxation.

After the relaxation calculation is finished, copy the relaxed structure in CONTCAR to POSCAR-unit.

####Note: need to adjust parameter `NPAR` or `NCORE` in `INCAR` depending on the number of cores used. Each run uses 4 cores by default. Set `NPAR=SQRT(NCORES)`for optimal performance. To set input parameters in `INCAR`, do

```python 
paramas=v.params
params["NSW"]=2
v.INCAR_writer(v.params,subdir + "/INCAR")
```

## Description of Files 

### conda-env.yml
Can be used to generate the proper conda environment for these calculations. On Cannon, first do `module load python`, and then `conda env create -f conda-env.yml`. The created environment will have the name `atomate_env`.

### multilayer_config_generator.py
#### MultilayerSet class
Tool which takes all possible monolayer POSCAR files in specified directory and generates all possible multilayer POSCAR files with 1-5 layers in a specified directory.
#### RelaxedBilayerMultilayerSet
Tool which takes all relaxed bilayers in an output file and uses the optimized vertical separations and angles to generate all possible pre-optimized trilayers.

### vasp_config.py
tool to combine layers according to the `config` file

### relax.py
creates directories for all bilayer combinations at 15 interlayer separations to prepare for vasp runs

### bat_vasp
calls VASP executable in each subfolder for individual VASP runs

### bat1_vasp
calls VASP executable in each subfolder, in cases where relative directory for `vasp.std` is different than in `bat_vasp`.

### relax_run.batch
calls `bat_vasp` in individual subfolder created by `relax.py`

### vasp_out.py
post-processes the output from VASP, fit E0 vs. z and find the interlayer separation corresponding to the minimum ground energy, submit another VASP calculation to relax atoms to the optimal positions at the optimal z

### vasp_out.batch
Batch file to call `vasp_out.py`

### cleanup.py:
Collects data from the final VASP run created by `vasp_out.py` and creates phonopy configuration files. Stores all the input information in folder `/phonopy_inputs`

### cleanup.batch
runs `cleanup.py`

### phonopy_params.conf
Contains parameters for the phonopy calculation: `DIM`, `BAND`, `BAND_POINTS`, and `MP`. See phonopy documentation for details on these parameters.

### phonopy_config_generator.py
Given a bilayer configuration file, generates `band.conf` and `mesh.conf`, which are files necessary to post-process VASP force field calculations and generate data (in `.hdf5` format) on the phonon band structure.

### preprocess.py
Copies over results from VASP interlayer relaxation and makes sure all necessary input files for final VASP force field calculation are present.

### preprocess.batch
Runs `preprocess.py`, then calls batch script `forces.batch`.

### forces_vasp.py
Given a directory of directories, with each inner directory corresponding to a multilayer material:
1. Generates phonopy displacement supercells (e.g. `POSCAR-001`)
2. Runs force field VASP calculations on each phonopy displacement supercell.

### forces.batch
Runs `forces_vasp.py`, then calls batch script `postprocess.batch`.

### postprocess.py
Generates `.hdf5` files based on the output of the VASP force field calculation. Writes these files to `/n/holyscratch01/cs205/group4/example-ff/`

### postprocess.batch
Runs `postprocess.py`.

## Folder `/PPs`
Contains pseudopotential files for different elements. `vasp_config.py` combines them into 1 `POSCAR` for different material combinations. 


## Results 
Our results for optimal interlayer separation are based on ~5500 VASP calculations for 0-degree bilayers and ~1500 for 180-degree bilayers. 



Our results show that the optimal interlayer separation varies drastically depending on the element composition. A larger atomic number results in a smaller interlayer separation. 
