# Create VASP inputs files and combine monolayer TMDCs

Edit ` ``config`` ` file as needed 

#### Default  ` ``config`` ` file format: 
Each layer has four lines. 

Line 1: elements (order: metal, chalcogen)

Line 2: number of atoms corresponding to the element above 

Line 3: layer alignment with respect to the positive x axis (0 degree or 180 degrees, or equivalently, alignment or anti-alignment)

Line 4: Layer separation between this layer and the last layer. The separation is defined as the distance between the chalcogen atom of the layer ($\ell$-1) to the metal atom of the layer $\ell$


To construct the structure, do

`import vasp_cofig as vc`

`v = vc.Vasp_Config()` 

To write `POSCAR` and `POTCAR`, do 

`vc.POSCAR_writer()`

`vc.POTCAR_writer()`
