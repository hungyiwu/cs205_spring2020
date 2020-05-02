# Create VASP inputs files and combine monolayer TMDCs

To run the work flow, first do 

`sbatch zscan.batch`, which runs 20 vasp calculations at different interlayer separations 

Then do `sbatch bat`, which first extract the optimal interlayer separation and do a relaxation calculation at the optimal spacing, and copies the output structure and creates the INCAR for the force field calculation


### General Workflow
0. Create different config files using the MultilayerSet class in `multilayer_config_generator.py`
1. Combine different layers using the input in `config` and create VASP input files
2. Run VASP multiple calculations at different interlayer separation files that allows ions to move in the z-direction to find optimal interlayer separations 
3. Fit the ground state energy vs. the interlayer separation as a function of z to a parabolic function. Extract the optimal interlayer separation 
4. Perform a relaxation calculation at the optimal interlayer spearation. Copy the geometry to `/phonopy_inputs/' folder 
5. Copy the relaxed structure to `POSCAR-unit`, rewrite `INCAR-ff` for the force field calculation (same setting except for letting `NSW=1` for no ionic relaxation)

Edit `config` file as needed 

#### Default  `config` file format: 
Each layer has four lines. 

Line 1: elements (order: metal, chalcogen)

Line 2: number of atoms corresponding to the element above 

Line 3: layer alignment with respect to the positive x axis (0 degree or 180 degrees, or equivalently, alignment or anti-alignment)

Line 4: Layer separation between this layer and the last layer. The separation is defined as the distance between the chalcogen atom of the layer ($\ell$-1) to the metal atom of the layer $\ell$

To construct config files, use the multilayer_config_generator.py file. Read class variables for specifics. See quickrunner.py for example run which combines TMDC_poscar monolayers into the multilayer permutations with repetition of up to 3 stacks in multilayer_TMDC_poscar.

To construct the structure, do

`import vasp_cofig as vc`

`v = vc.Vasp_Config()` 

To write `POSCAR`, `POTCAR`, `KPOINTS`, and `INCAR` do 

`vc.POSCAR_writer()`

`vc.POTCAR_writer()`

`vc.KPOINTS_writer()`

`vc.KPOINTS_writer(v.params)`

Use and `params.config` from the phonopy pipeline to run initialize filepath, conda environment etc.

After the structure construction, perform a VASP calculation to allow out-of-plane relaxation.

After the relaxation calculation is finished, copy the relaxed structure in CONTCAR to POSCAR-unit.

### Note: need to adjust parameter `NPAR` or `NCORE` in `INCAR` depending on the number of cores used. Each run uses 4 cores by default. 
