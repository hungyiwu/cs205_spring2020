# Term project of CS205 Spring 2020, group 4: *Ab initio* phonon calculation in layered two-diensional materials


## Introduction
Two-dimensional materials (2D) are a class of atomically thin materials. The most famous example is graphene, which is a hexagonal lattice. These 2D materials have a wide range of physical properties. For example, hexagonal Boron Nitrice (hBN) is an insulator and is commonly used as a substrate experiment; transitition metal dichalcogenides (TMDCs) such as MoS_2 are semiconductors. 
These 2D layered materials have become a favorite platform to manipulate their physical properties. Recently, people have been exploring van der Waals heterostructures, which refer to the layered assembilies of the 2D materials. They are mediated by long-range van der Waals interaction, and therefore are also called van der Waals heterostructures. The flexibility and available experimental control "knobs" make them an ideal platform to explore strongly correlated physics 

![Periodic table](https://cdn.britannica.com/45/7445-050-CA28EA33/version-periodic-table-elements.jpg)

# Software Installation
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


## Codes

## Test Case
Test runs are in branch `example`. 

## Results

## References 
