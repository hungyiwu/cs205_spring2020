# Create VASP inputs files and combine monolayer TMDCs

Edit `config` file as needed 

To run the work flow, do `sbatch bat`

### General Workflow
1. Combine different layers using the input in `config` and create VASP input files
2. Run VASP calculation that allows ions to move in the z-direction to find optimal interlayer separations
3. Copy the relaxed structure to `POSCAR-unit`, rewrite `INCAR-ff` for the force field calculation (same setting except for letting `NSW=1` for no ionic relaxation)

#### Default  `config` file format: 
Each layer has four lines. 

Line 1: elements (order: metal, chalcogen)

Line 2: number of atoms corresponding to the element above 

Line 3: layer alignment with respect to the positive x axis (0 degree or 180 degrees, or equivalently, alignment or anti-alignment)

Line 4: Layer separation between this layer and the last layer. The separation is defined as the distance between the chalcogen atom of the layer ($\ell$-1) to the metal atom of the layer $\ell$


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
