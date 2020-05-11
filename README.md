# Term project of CS205 Spring 2020, group 4
## *Ab initio* phonon calculation in layered two-diensional materials

## Introduction
Two-dimensional materials (2D) are a class of atomically thin materials. The most famous example is graphene, which is a hexagonal lattice. These 2D materials have a wide range of physical properties. For example, hexagonal Boron Nitrice (hBN) is an insulator and is commonly used as a substrate experiment; transitition metal dichalcogenides (TMDCs) such as MoS2 are semiconductors. 
These 2D layered materials have become a favorite platform to manipulate their physical properties. Recently, people have been exploring van der Waals (vdW) heterostructures, which refer to the layered assembilies of the 2D materials. They are mediated by long-range vdW interaction, and therefore are also called vdW heterostructures. The flexibility and available experimental control "knobs", such as the material combination, relative twist angle, displacement field, and magnetic field, make them an ideal platform to explore strongly correlated physics. For example, strongly correlated insulator states and unconventional superconductivity were observed in twisted bilayer graphene [[1]](#1)[[2]](#2), whose microscopic origin remains an open question. In this project, we develop a workflow to systematically calculate the phonon of layered heterostructures, specifically multi-layered TMDCs. This serves as the first step to investigate the role that phonon plays in the correlated states. 

<img src="https://upload.wikimedia.org/wikipedia/commons/9/9b/1D_normal_modes_%28280_kB%29.gif" width="250"> [Image source: Wikipedia]

TMDC is a type of 2D materials, whose unit cell is consisted of 1 transition metal (group 4 - group 12 in the periodic table) and 2 chalcogen atoms (S, Se, Te). The chalcogen atoms and the transition metal are not on the same vertical plane. It is a semiconductor with physical properties that are drastically different than graphene. Like graphene, it is a hexagonal lattice, but its inversion symmetry is broken. Below is a top view and side view of monolayer WTe2. 

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/wse2_mono.png" width="200">
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/wse2_mono_side.png" width="200">


Phonons are collective excitations in solids, which are long-ranged lattice vibrations from the equilibrium. Phonon modes are responsible of creating attractive interaction that mediate superconductivity according to BCS theory or Bardeen–Cooper–Schrieffer theory. Here is an example showing different normal modes of lattice vibration in a 1D chain. 

<img src="https://upload.wikimedia.org/wikipedia/commons/9/9b/1D_normal_modes_%28280_kB%29.gif" width="250">

Similarly, here is a visualization of how phonon mode propages through a 2D solid: 

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/400px-Lattice_wave.svg.png" width="250">
[Imgage source: Wikipedia] 

Our calculations are based on Density Functional Theory (DFT), which is first-principles quantum mechanical model that computes electronic properties by solving the Scrhodinger's equation. Instead of using the full many-body wave function as the basis, it uses the electron density as the basis. According to Kohn-Sham theory, there is an one-to-one correspondence between the many-body wavefunction to electron density. This turns the many-body Schrodinger's equation to a so-called "Kohn-Sham Hamiltonian" that only involves electron density. The "Kohn-Sham Hamiltonian" is exact, with unknown exchange-correlation functionals. In our project, we use a commercial DFT Vienna Ab initio Simulation Package (VASP) [[3]](#3).

In DFT calculations, one needs to choose the exchange-correlation functional depending on the system of interest. Since the layered-materials involve vdW interactions, which is long-ranged and non-local by nature, we need to choose vdW functionals. Here, we use `SCAN+rVV10` functional, which is both accurate and computationally efficient [[4]](#4). 

For the phonon spectrum, we use the Python packge `phonopy`, which uses the force field computed from DFT and use finite difference to calculate the phonon properties [[5]](#5). 

Our projects involve both big compute and big data, combining both high-throughput and high-performance computing. For each DFT calculation, we are using distributed memory parallelism through MPI, and using thread-level parallelism by running multiple DFT calculations concurrently. Finally, we use Spark Dataframe to analyze the data.

## Software Installation and Test Case 
The guide assumes you are on using Harvard Cannon. 


#### Before you start 
- Make a conda environment with `conda-env.yml`.
- Edit `params.config` to change the conda environment name 
- Make sure `vasp.std` is in this folder
- Confirm that Python package `pymatgen` is installed in the active environment.

#### Steps to run, assuming you are setup on Cannon and have read/write access to `/n/holyscratch/cs205/group4`:
1. Set up a conda environment, which must minimally contain:
- python
- phonopy (from conda-forge)
- h5py (from conda-forge)
- pymatgen
- hdf5

On Cannon, you can do: 
```bash 
module load python
```
and then
```bash
conda env create -f conda-env.yml
```
Note: modify `name` to change the conda environment name and chance the directory for `prefix` to your home directory

2. Move to the `/inputs/` directory. Before running to workflow, create two directories to store raw data from the vasp run 
```bash 
mkdir vasp_relax_test 
mkdir vasp_relax 
```
Run the first portion of the pipeline (multilayer creation and relaxation) by doing: 
```bash 
sbatch zscan.batch
```
This will create 15 VASP calculations in folder `/vasp_relax_test`, and extract the data from this folder, create a final VASP calculation based on the optimal interlayer spacing in folder `/vasp_relax`, and generate output for phonon calculations. The final outputs will be written to `/n/holyscratch01/cs205/group4/example-relax/`

3. Run the second porition of the pipeline (phonopy and force field calculation) by doing: `sbatch preprocess.batch`. The final outputs will be written to `/n/holyscratch01/cs205/group4/example-ff/`.

4. Examine the results with Spark code in the `/outputs/` directory. Since the VASP calculation in the first part can take a very long time, we have put an example output file for one material in the `/outputs/` directory, so that this code can be tested without waiting for the VASP calculations to finish. To run the Spark code, do (in `/outputs/`):
```bash
module load jdk/10.0.1-fasrc01
```
Then, download spark (e.g. by following instructions in the course guide: https://harvard-iacs.github.io/2020-CS205/lab/I9/guide/Guide_I9.pdf), or by doing: 
```bash
sudo curl -O http://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz
```
and then copying the `.tgz` file to the Cannon directory. Then, unzip the `.tgz` file: 
```bash
tar xvf spark-2.2.0-bin-hadoop2.7.tgz
```
Finally, run the example: 
```bash
./spark-2.2.0-bin-hadoop2.7/bin/spark-submit example.py .
```
The output of this example will be the filename and the band gap of the material.


## General Workflow

1. Curate a list of TMDC (**T**ransition **M**etal **D**ichal**C**ogenide) of interest

   Get the list of stable 2D material from the Materials Cloud, lattice constants (in downloaded POSCAR files) from the Materials Project.
   
2. Combine mono-layer unit cells to multi-layer unit-cells

   Combinatorial, with different orientations.
   
3. Determine optimal spacing for mono-layer unit cells

```
# Python-flavored pseudo-code

def generate_unitcell_POSCAR(formula, lattice_constant, template_POSCAR_file):
    possible_spacing = [1, 2, 3]
    energy = []
    
    for spacing in possible_spacing:
        initial_POSCAR_file = write_POSCAR_file(formula, lattice_constant, template_POSCAR_file, spacing)
        candidate_VASP_result = run_VASP_to_relax_structure(initial_POSCAR_file)
        candidate_energy = calculate_energy(candidate_VASP_result)
        energy.append(candidate_energy)
        
    min_energy_spacing = possible_spacing[np.argmin(energy)]
    unitcell_POSCAR_file = write_POSCAR_file(formula, lattice_constant, template_POSCAR_file, min_energy_spacing)
    
    return unitcell_POSCAR_file
```
   
4. Pre-processing using `phonopy`

   `[list of displacement] = run_phonopy_preprocessing(multilayer_unitcell_POSCAR, dimensions)`
   
5. Calculate force-field of multi-layer materials by VASP

   One Slurm job for each displacement from step 4. Slurm will do load balancing.
   
6. Post-processing using `phonopy`

   `band_structure.hdf5 = run_phonopy_postprocessing(list_of_displacement_forcefield, band.conf)`  
   `DoS.hdf5 = run_phonopy_postprocessing(list_of_displacement_forcefield, mesh.conf)`
   
7. Parse band gap results using Spark

   Parse band gap results from step 6 and perform speed-up assessment on the Spark script.
  
## Breakdown of Workflow

0. Create different config files using the MultilayerSet class in `multilayer_config_generator.py`, which save the data that contains the given metal, chalcogen, with the given ali
3b. Use the RelaxedBilayerMultilayerSet class to collect optimal vertical separations and alignments from the initial VASP calculation output files and obtain more precisely relaxed trilayers.
4. Perform a relaxation calculation at the optimal interlayer spearation. Copy the geometry to `/phonopy_inputs/' folder 
5. Copy the relaxed structure to `POSCAR-unit`, rewrite `INCAR-ff` for the force field calculation (same setting except for letting `NSW=1` for no ionic relaxation)
6. Generate phonopy supercells based on `POSCAR-unit` (number of supercells depends on symmetry/space group of structure).
7. Run a VASP force field calculation on each supercell.
8. Process the results using phonopy to generate `.hdf5` files containing band structure information.


### List of 2D material

We curated the input data by first querying the Material Project database for lattice dimension data (POSCAR files) containing only the elements of interest, and then filter them by a list of known 2D materials downloaded from the Material Cloud website.

source: https://www.materialscloud.org/discover/2dstructures/dashboard/list

### Relaxation
In this step, we sample 15 different interlayer spacings between bilayers (aligned/0-deg. or antialigned/180.deg) in order to find the optimal positions between each pair of layers. The outputs generated include: 
1. the list of optimal interlayer spacing `zoptlist.txt` 
2. ground state energy vs. interlayer spacing  `zElist.txt` 
3. Input parameters for phonopy calculations in folder `/phonopy_inputs`

### Analyzing the output data from relaxation

To parse the output files and plot the results from `zElist.txt` and `zoptlist.txt`, run

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit zEanalysis_spark.py`. This will generates three figures and   save to the `results` folder

<p float="left">
  <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_TeTe.png" width="400">
  <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/E0_TeTe.png" width="400">
</p>
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/E0_vs_z_TeTe.png" width="400">

This particular script groups the materials by chalcogens. We use Spark to organize the data. A speedup test using Spark dataframe is    contained in the folder `/zEanalysis`. To run a speedup test, do  

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit select_zEdata.py <<metal>> <<chalcogen>> <<alignment>>        <<np>>`.

which save the data that contains the given metal, chalcogen, with the given alignment (0 degree or 180 degrees), and <<np>> is the      number of cores to use. For example,  

`<<spark-directory-on-Cannon>>//spark-2.2.0-bin-hadoop2.7/bin/spark-submit select_zEdata.py Mo S 0 4`

### Phonopy and VASP force field calculations

Given a set of relaxed multilayer structures, as created in the first step (which ends with `cleanup.batch`/`cleanup.py`), to run the phonopy and VASP force field calculations do:
1. Ensure that the directory containing the results from the first step is on the Cannon $SCRATCH directory (e.g. on `/n/holyscratch01/cs205/group4/<directory>`. This ensures that you don't fill up your home directory with large files.
2. Edit line 7 of `preprocess.py` to ensure that this script is reading the data from the correct directory. If desired, edit line 10 to change the force field directory (if you do, you must also change line 10 and line 7 in `forces_vasp.py` and `postprocess.py`, respectively). 
3. If desired, change `NPAR` in `preprocess.py` to run with different numbers of cores. If so, change `-n` in `bat1_vasp` to be `NPAR`^2. 

To run the entire workflow for this section, do: `sbatch preprocess.batch`. The results (in `.hdf5` format) will be written to the `$OUTPUTFILE_PATH` directory specified in `params.conf`.


## Code Descriptions
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

### Folder `/PPs`
Contains pseudopotential files for different elements. `vasp_config.py` combines them into 1 `POSCAR` for different material combinations. 

## Results

The optimized vertical stacking height (optimized for lowest energy configuration) for numerous TMDCs was calculated. The general trend is that chalcogens with a larger atomic number (that is, larger atoms with more protons and electrons), have larger optimal vertical stacking heights. Below we have the graphs of various TMDCs, each of which contain a common chalcogen, in order of increasing atomic number, S, Se, Te.

<p float="left">
  <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_SS.png" width="400">
   <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_SeSe.png" width="400">
</p>
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_TeTe.png" width="400">

We also see that optimized vertical stacking is a function of alignment angle. Anti-aligned (180 degrees) bilayers have shorter stacking distances than aligned (0 degrees) structures. This is due to less overlap between structures with similar electronic configurations (i.e. identical atoms overlapped on top of one another can be thought to "repel", raising the energy levels). Below we have aligned and anti-aligned bilayers with Se chalcogens that display this tendency.
#### Aligned: 
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_SeSe.png" width="500">

#### Anti-aligned
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/z_SeSe_180.png" width="500">

The final products of our VASP calculations are phonon band structures (energy of states E vs wave vector k), density of states which is proportional to dE/dk (the density of states with a given energy value which is larger when the band structure is flatter). Below we have the band structure and corresponding density of states for WSe2.


<p float="left">
    <img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/bands_wse2_bi.png" height="400">
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/dos_wse2_bi.png" height="400">
</p>


In addition to these features, we also see the presence of a band gap, or region between two groupings of bands where no state bands can cross. Below is a plot of the size of these band gaps for various TMDC bilayers.

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/samechalc_bg.png" width="600">

## Performance Evaluation

The central phonon calculations were done using VASP, a software package that is based on MPI. The performance of MPI is heavily dependent of the number of nodes used, with more nodes being able to divide the work into smaller portions but also requiring more overhead, such as data sharing and message passing. Below is a plot for large scale VASP (MPI) calculations with various numbers of cores. The execution time decrease/speedup is linear until more than 25 cores is reached, at which point the speedup begins to slow.

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/speedup.png" width="600">

The Big Data applications of this project were ran using Spark. While Sparks multicore design can lead to considerable speedup, it can also result in needless overhead when the number of cores used is too great for the size of the data set evaluated. This is shown in the graphs below for optimized vertical spacing data processing for a data set of approximately 10 Mb. While execution time grows and speedup increases for 4 and fewer cores, performance actually suffers for larger numbers of cores, showing that the overhead has outweighted the efficiency of added processors.

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/spark_speedup.png" width="600">

This same phenomena can be observed when using Spark to obtain band gap data from various output files. In the graph below, the performance of large numbers of cores (4 and 8) improves when the data set becomes large, showing markedly smaller execution times than the local, single core implementation. However, the 2 core implementation actually displays worse performance than the local version, as its multicore design introduces more overhead than its merely 2 core archetecture can remediate in actual speedup.

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/Image from iOS.jpg" width="600">

## Benchmark and Conclusion
Finally, we compared our obtained band structure for bilayers to the known results in [[6]](#6) and we observe similar band structures as their Fig. 2. However, the systematic study of multi-layered 2D vdW heterostructures has not been performed, which makes our project a valuable addition to the study of vdW heterostructures. For future directions, a more exhaustive exploration to explore the parameter space of material combination is needed, such as including three or more layesr, which would require more computing resources. 

## References 
<a id="1">[1]</a> 
Cao, Yuan, et al. "Unconventional superconductivity in magic-angle graphene superlattices." Nature 556.7699 (2018): 43-50.

<a id="1">[2]</a> 
Cao, Yuan, et al. "Correlated insulator behaviour at half-filling in magic-angle graphene superlattices." Nature 556.7699 (2018): 80.

<a id="1">[3]</a> 
VASP: https://www.vasp.at/

<a id="1">[4]</a> 
Peng, Haowei, et al. "Versatile van der Waals density functional based on a meta-generalized gradient approximation." Physical Review X 6.4 (2016): 041005.

<a id="1">[5]</a> 
Atsushi Togo and Isao Tanaka, "First principles phonon calculations in materials science", Scr. Mater., 108, 1-5 (2015)
https://phonopy.github.io/phonopy/index.html

<a id="1">[6]</a> 
Zhang, Xin, et al. "Phonon and Raman scattering of two-dimensional transition metal dichalcogenides from monolayer, multilayer to bulk material." Chemical Society Reviews 44.9 (2015): 2757-2785.
