import os
import sys
import re
import shutil

def write_submit_job(job_name, job_folderpath, vasp_filepath,
        job_filename='job.sbatch', n=6, t='0-01:00', p='shared,test', mem_per_cpu='4G'):
    # convert to absolute paths
    job_folderpath = os.path.abspath(job_folderpath)
    vasp_filepath = os.path.abspath(vasp_filepath)

    # format job text
    job_text = [
            '#!/bin/bash',
            '#SBATCH --job-name={}'.format(job_name),
            '#SBATCH -n {}'.format(n),
            '#SBATCH -t {}'.format(t),
            '#SBATCH -p {}'.format(p),
            '#SBATCH --mem-per-cpu={}'.format(mem_per_cpu),
            '#SBATCH -o {}_%j.out'.format(job_name),
            '#SBATCH -e {}_%j.err'.format(job_name),
            '#SBATCH --account=cs205',
            'module load intel impi',
            'cd {}'.format(job_folderpath),
            'mpirun -np {} {}'.format(n, vasp_filepath),
            ]

    # write job script
    job_filepath = os.path.join(job_folderpath, job_filename)
    with open(job_filepath, 'w') as outfile:
        outfile.writelines([line+'\n' for line in job_text])

    # return bash command for submission
    return job_filepath

if __name__ == '__main__':
    # params
    vasp_filepath, run_filepath = sys.argv[1], sys.argv[2]
    misc_filename_list = ['INCAR', 'POTCAR', 'KPOINTS']

    # find all supercell files
    supcell_filename_list = [n for n in os.listdir()\
            if re.fullmatch(pattern='POSCAR-\d{3}', string=n) is not None]

    job_queue = []
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
        job_filepath = write_submit_job(job_name=index,
                job_folderpath=supcell_folderpath,
                vasp_filepath=vasp_filepath)
        job = 'jid{}=$(sbatch {})'.format(len(job_queue), job_filepath)
        job_queue.append(job)

    # add post-processing job that depends on all previous jobs
    job = 'sbatch --dependency=afterok:' + ':'.join(['$jid{}'.format(i)\
            for i in range(len(job_queue))]) + ' postprocessing.sbatch'
    job_queue.append(job)

    # write execution bash script to disk
    with open(run_filepath, 'w') as outfile:
        outfile.writelines([line+'\n' for line in job_queue])
