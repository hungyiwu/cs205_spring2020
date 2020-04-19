import vasp_config as vc 
import sys 

v = vc.Vasp_Config()
incar_params = v.params
incar_params.params["NSW"]=1

v.INCAR_writer(incar_params)

os.sys("mv CONTCAR POSCAR-unit")
