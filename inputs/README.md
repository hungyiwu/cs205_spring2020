# Create VASP inputs files and combine monolayer TMDCs
## Before you start 
- Make a conda environment with `conda-env.yml`.
- Edit `params.config` to change the conda environment name 
- Make sure `vasp.std` is in this folder
- Confirm that Python package `pymatgen` is installed in the active environment.



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

## Results 
Our results for optimal interlayer separation are based on ~5500 VASP calculations for 0-degree bilayers and ~1500 for 180-degree bilayers. 



Our results show that the optimal interlayer separation varies drastically depending on the element composition. A larger atomic number results in a smaller interlayer separation. 
