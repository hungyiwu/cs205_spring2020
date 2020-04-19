import vasp_config as vc 

v = vc.Vasp_Config()
v.POSCAR_writer()
v.POTCAR_writer()
v.KPOINT_writer()
v.INCAR_writer(v.params)

vasp_filepath = sys.argv[1]
v.vasp_run(vasp_dir=vasp_filepath)

