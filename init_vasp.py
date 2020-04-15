import os
import sys
import re
import shutil
import subprocess

def write_submit_job(job_name, job_folderpath, vasp_filepath,
        n=6, t='0-01:00', p='shared,test', mem_per_cpu='4G'):
    # format job text
    job_text = [
            '#!/bin/bash',
            '#SBATCH --job-name={}'.format(job_name),
            '#SBATCH -n {}'.format(n),
            '#SBATCH -t {}'.format(t),
            '#SBATCH -p {}'.format(p),
            '#SBATCH --mem-per-cpu={}'.format(mem_per_cpu),
            '#SBATCH -o job_%j.out',
            '#SBATCH -e job_%j.err',
            '#SBATCH --account=cs205',
            'module load intel impi',
            'mpirun -np {} {}'.format(n, vasp_filepath),
            ]

    # write job script
    job_filename = 'job.sbatch'
    job_filepath = os.path.join(job_folderpath, job_filename)
    with open(job_filepath, 'w') as outfile:
        outfile.writelines([line+'\n' for line in job_text])

    # submit job from its folder
    subprocess.call(['sbatch', job_filename], cwd=job_folderpath)

    return

if __name__ == '__main__':
    # params
    vasp_filepath = sys.argv[1]
    misc_filename_list = ['INCAR', 'POTCAR', 'KPOINTS']

    # find all supercell files
    supcell_filename_list = [n for n in os.listdir()\
            if re.fullmatch(pattern='POSCAR-\d{3}', string=n) is not None]

    for supcell_filename in supcell_filename_list:
        # make folder
        index = supcell_filename.split('-')[1]
        supcell_folderpath = 'supcell_{}'.format(index)
        os.mkdir(supcell_folderpath)

        # copy POSCAR file
        dst = os.path.join(supcell_folderpath, 'POSCAR')
        shutil.copyfile(supcell_filename, dst)

        # copy misc cells
        for misc_filename in misc_filename_list:
            dst = os.path.join(supcell_folderpath, misc_filename)
            shutil.copyfile(misc_filename, dst)

        # build vasp job script
        write_submit_job(job_name=index,
                job_folderpath=supcell_folderpath,
                vasp_filepath=vasp_filepath)
