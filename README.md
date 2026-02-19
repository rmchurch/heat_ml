# heat_ml
Repo with data generation and more needed for HEAT machine learning

## Data generation
`run_heat_mpicommexecutor.sh` and `heat_mpicommexecutor.py` are used to run embarrasingly parallel data generation of HEAT simulations. This uses the `mpi4py` package `MPICommExecutor` to spin up an executor which will send tasks to workers, and continually feed the workers tasks as they complete. 
