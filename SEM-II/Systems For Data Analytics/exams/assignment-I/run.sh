#!/bin/bash
echo -e "\nProcessing geosales.csv in parallel using $1 processes\n"
echo -e "Chunking geosales.csv into $1 files\n"
python3.10 split.py $1
echo -e "Processing each chunk in parallel using MPI framework\n"
mpiexec -n $1 python3.10 mpi_compute.py