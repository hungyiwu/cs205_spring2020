# Term project of CS205 Spring 2020, group 4
## *Ab initio* phonon calculation in layered two-diensional materials

## Introduction
Two-dimensional materials (2D) are a class of atomically thin materials. The most famous example is graphene, which is a hexagonal lattice. These 2D materials have a wide range of physical properties. For example, hexagonal Boron Nitrice (hBN) is an insulator and is commonly used as a substrate experiment; transitition metal dichalcogenides (TMDCs) such as MoS_2 are semiconductors. 
These 2D layered materials have become a favorite platform to manipulate their physical properties. Recently, people have been exploring van der Waals (vdW) heterostructures, which refer to the layered assembilies of the 2D materials. They are mediated by long-range vdW interaction, and therefore are also called vdW heterostructures. The flexibility and available experimental control "knobs", such as the material combination, relative twist angle, displacement field, and magnetic field, make them an ideal platform to explore strongly correlated physics. For example, strongly correlated insulator states and unconventional superconductivity were observed in twisted bilayer graphene, whose microscopic origin remains a open question. In this project, we develop a workflow to systematically calculate the phonon of layered heterostructures, specifically multi-layered TMDCs. This serves as the first step to investigate the role that phonon plays in the correlated states. 

Phonons are collective excitations in solids, which are long-ranged lattice vibrations from the equilibrium. Phonon modes are responsible of creating attractive interaction that mediate superconductivity according to BCS theory or Bardeen–Cooper–Schrieffer theory. Here is an example showing different normal modes of lattice vibration in a 1D chain. 

![phonon](https://upload.wikimedia.org/wikipedia/commons/9/9b/1D_normal_modes_%28280_kB%29.gif)

Similarly, here is a visualization of how phonon mode propages through a 2D solid: 

![2Dphonon](https://github.com/hywu0110/cs205_spring2020/blob/develop/results/geom/400px-Lattice_wave.svg.png)
[Imgage source: Wikipedia] 



Our calculations are based on Density Functional Theory (DFT), which is first-principles quantum mechanical model that computes electronic properties by solving the Scrhodinger's equation. Instead of using the full many-body wave function as the basis, it uses the electron density as the basis. According to Kohn-Sham theory, there is an one-to-one correspondence between the many-body wavefunction to electron density. This turns the many-body Schrodinger's equation to a so-called "Kohn-Sham Hamiltonian" that only involves electron density. The "Kohn-Sham Hamiltonian" is exact, with unknown exchange-correlation functionals. In DFT calculations, one needs to choose the exchange-correlation functional depending on the system of interest. 

Since the layered-materials involve vdW interactions, which is long-ranged and non-local by nature, we need to choose vdW functionals. Here, we use `SCAN+rVV10` functional, which is both accurate and computationally efficient. https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.041005 

For the phonon spectrum, we use the Python packge `phonopy`, which uses the force field computed from DFT and use finite difference to calculate the phonon properties. 

Our projects involve both big compute and big data, combining both high-throughput and high-performance computing. For each DFT calculation, we are using distributed memory parallelism through MPI, and using thread-level parallelism by running multiple DFT calculations concurrently. Finally, we use Spark Dataframe to analyze the data.

![Periodic table](https://cdn.britannica.com/45/7445-050-CA28EA33/version-periodic-table-elements.jpg)

## Software Installation
The guide assumes you are on using Harvard Cannon. 


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

source: https://www.materialscloud.org/discover/2dstructures/dashboard/list


## Code Descriptions

## Test Case
Test runs are in branch `example_runs`. 

## Results

## Performance Evaluation

## References 
