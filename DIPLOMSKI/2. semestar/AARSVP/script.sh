#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output=job_%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=00:10:00

for threads in 1 2 4 8 12 16
do
    export OMP_NUM_THREADS=$threads
    echo "Use $OMP_NUM_THREADS threads:"
    ./optimizirano
    echo ""
done