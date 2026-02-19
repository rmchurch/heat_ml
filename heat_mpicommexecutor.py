import subprocess
import glob
import os
from mpi4py import MPI
from mpi4py.futures import MPICommExecutor
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def run_heat(idi, batch_file_path):

    # Construct the command line
    cmd = 'apptainer run --bind $HOME /home/rmc2/HEAT/heat_v3.2_root.sif /home/rmc2/HEAT/test_heat.sh {}'.format(batch_file_path)
    print("    "+cmd)
    # Run the command using the executor
    result = subprocess.run(cmd, shell=True)#, capture_output=True, text=True)

    return result


def gen_batchfiles():
    basedir = '/home/rmc2/SPARC/'
    files = glob.glob(basedir + 'sparc/eqdsk/*')
    files.sort()
    
    ## STEP 1: Write batchFile for each geqdsk
    #get the template file. Will need to write the last line for each geqdsk file
    f = open(basedir+'batchFile_template.dat','r')
    lines = f.readlines()
    f.close()

    for ifi,file in enumerate(files):
        eqfilebase = os.path.basename(file)
        eqfilebasenosuff = os.path.splitext(eqfilebase)[0]
        newbatchfile = (basedir + 'batchFile_%04d.dat' % ifi)
        with open(newbatchfile,'w') as fnew:
            for line in lines:
                fnew.write(line)
            fnew.write('sparc,%s,eqdsk/%s,10degPFCsector_20231025.step,pfc_carrier_input_BAobjs.csv,SPARC_input.csv,hfOpt' % (eqfilebasenosuff,eqfilebase))
        yield ifi, newbatchfile

def log_completion(future):
    result = future.result()
    job_id = future.job_id
    return_code = result.returncode
    if return_code == 0:
        logging.info(f"Subprocess successfuly for job {job_id} completed with return code {return_code}")
    else:
        logging.info(f"Subprocess FAILED for job {job_id} completed with return code {result.stderr}")


if __name__=="__main__":
    with MPICommExecutor(MPI.COMM_WORLD, root=0) as executor:
        if executor is not None:
            logging.info("Begin running root")
            futures = []
            for job_id,filei in gen_batchfiles():
                future = executor.submit(run_heat, job_id, filei)
                future.job_id = job_id
                future.add_done_callback(log_completion)
