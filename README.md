# Term project of CS205 Spring 2020, group 4
## *Ab initio* phonon calculation in layered two-diensional materials

## Introduction
Two-dimensional materials (2D) are a class of atomically thin materials. The most famous example is graphene, which is a hexagonal lattice. These 2D materials have a wide range of physical properties. For example, hexagonal Boron Nitrice (hBN) is an insulator and is commonly used as a substrate experiment; transitition metal dichalcogenides (TMDCs) such as MoS_2 are semiconductors. 
These 2D layered materials have become a favorite platform to manipulate their physical properties. Recently, people have been exploring van der Waals (vdW) heterostructures, which refer to the layered assembilies of the 2D materials. They are mediated by long-range vdW interaction, and therefore are also called vdW heterostructures. The flexibility and available experimental control "knobs", such as the material combination, relative twist angle, displacement field, and magnetic field, make them an ideal platform to explore strongly correlated physics. For example, strongly correlated insulator states and unconventional superconductivity were observed in twisted bilayer graphene, whose microscopic origin remains an open question. In this project, we develop a workflow to systematically calculate the phonon of layered heterostructures, specifically multi-layered TMDCs. This serves as the first step to investigate the role that phonon plays in the correlated states. 

<img src="https://cdn.britannica.com/45/7445-050-CA28EA33/version-periodic-table-elements.jpg" width="800">

TMDC is a type of 2D materials, whose unit cell is consisted of 1 transition metal (group 4 - group 12 in the periodic table) and 2 chalcogen atoms (S, Se, Te). The chalcogen atoms and the transition metal are not on the same vertical plane. It is a semiconductor with physical properties that are drastically different than graphene. Like graphene, it is a hexagonal lattice, but its inversion symmetry is broken. Below is a top view and side view of monolayer WTe2. 

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/wse2_mono.png" width="200">
<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/wse2_mono_side.png" width="200">


Phonons are collective excitations in solids, which are long-ranged lattice vibrations from the equilibrium. Phonon modes are responsible of creating attractive interaction that mediate superconductivity according to BCS theory or Bardeen–Cooper–Schrieffer theory. Here is an example showing different normal modes of lattice vibration in a 1D chain. 

<img src="https://upload.wikimedia.org/wikipedia/commons/9/9b/1D_normal_modes_%28280_kB%29.gif" width="250">

Similarly, here is a visualization of how phonon mode propages through a 2D solid: 

<img src="https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/400px-Lattice_wave.svg.png" width="250">
[Imgage source: Wikipedia] 

Our calculations are based on Density Functional Theory (DFT), which is first-principles quantum mechanical model that computes electronic properties by solving the Scrhodinger's equation. Instead of using the full many-body wave function as the basis, it uses the electron density as the basis. According to Kohn-Sham theory, there is an one-to-one correspondence between the many-body wavefunction to electron density. This turns the many-body Schrodinger's equation to a so-called "Kohn-Sham Hamiltonian" that only involves electron density. The "Kohn-Sham Hamiltonian" is exact, with unknown exchange-correlation functionals. In DFT calculations, one needs to choose the exchange-correlation functional depending on the system of interest. 

Since the layered-materials involve vdW interactions, which is long-ranged and non-local by nature, we need to choose vdW functionals. Here, we use `SCAN+rVV10` functional, which is both accurate and computationally efficient. https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.041005 

For the phonon spectrum, we use the Python packge `phonopy`, which uses the force field computed from DFT and use finite difference to calculate the phonon properties. 

Our projects involve both big compute and big data, combining both high-throughput and high-performance computing. For each DFT calculation, we are using distributed memory parallelism through MPI, and using thread-level parallelism by running multiple DFT calculations concurrently. Finally, we use Spark Dataframe to analyze the data.

## Software Installation
The guide assumes you are on using Harvard Cannon. 

#### Steps to run, assuming you are setup on Cannon and have read/write access to `/n/holyscratch/cs205/group4`:
1. Set up a conda environment, which must minimally contain:
- python
- phonopy (from conda-forge)
- h5py (from conda-forge)
- pymatgen
- hdf5

On Cannon, you can do: `module load python` and then `conda env create -f conda-env.yml`. 

2. Move to the `/inputs/` directory. Run the first portion of the pipeline (multilayer creation and relaxation) by doing: `sbatch zscan.batch`. The final outputs will be written to `/n/holyscratch01/cs205/group4/example-relax/`

3. Run the second porition of the pipeline (phonopy and force field calculation) by doing: `sbatch preprocess.batch`. The final outputs will be written to `/n/holyscratch01/cs205/group4/example-ff/`.

4. Examine the results with Spark code in the `/outputs/` directory. Since the VASP calculation in the first part can take a very long time, we have put an example output file for one material in the `/outputs/` directory, so that this code can be tested without waiting for the VASP calculations to finish. To run the Spark code, do (in `/outputs/`):
- `module load jdk/10.0.1-fasrc01`
- Download spark (e.g. by following instructions in the course guide: https://harvard-iacs.github.io/2020-CS205/lab/I9/guide/Guide_I9.pdf), or by doing: `sudo curl -O http://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz` and then coping the `.tgz` file to the Cannon directory.
- Unzip the `.tgz` file: `tar xvf spark-2.2.0-bin-hadoop2.7.tgz`
- Run the example: `./spark-2.2.0-bin-hadoop2.7/bin/spark-submit example.py .`
The output of this example will be the filename and the band gap of the material.


## Workflow

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
   
7. Calculate properties of interest (TBD) using Spark

   Use Spark to do operations for all 90 million (?) band structures and DoS from step 6 and calculate properties of interest.
  
## List of 2D material

We curated the input data by first querying the Material Project database for lattice dimension data (POSCAR files) containing only the elements of interest, and then filter them by a list of known 2D materials downloaded from the Material Cloud website.

source: https://www.materialscloud.org/discover/2dstructures/dashboard/list


## Code Descriptions
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

### Folder `/PPs`
Contains pseudopotential files for different elements. `vasp_config.py` combines them into 1 `POSCAR` for different material combinations. 



## Results

## Performance Evaluation

## References 
VASP: https://www.vasp.at/

Phonopy: https://phonopy.github.io/phonopy/index.html
