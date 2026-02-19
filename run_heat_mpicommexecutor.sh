#!/bin/bash
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=90
#SBATCH --cpus-per-task=1
#SBATCH --mem=201gb
#SBATCH --time=03:00:00
#SBATCH --qos=debug

cat $0 

conda activate default
srun --cpu-bind=cores python heat_mpicommexecutor.py
