#!/bin/sh

#SBATCH --job-name=test
#SBATCH --account=def-jphickey
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mem-per-cpu=4G
#SBATCH --output=test.log
#SBATCH --open-mode=append

module load python 3.11
module load openfoam/v2312
module load paraview/6.0.0

mpirun -np 64 redistributePar -parallel -decompose