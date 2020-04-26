import vasp_config as vc 
import os 

vasp_dir_new = '/vasp_relax/'


v = vc.Vasp_Config()
incar_params = v.params
incar_params["NSW"]=1

v.INCAR_writer(incar_params,fname='/INCAR-ff')

os.system("cp CONTCAR POSCAR-unit")
v.relax_off() # turn off selective dynamics
