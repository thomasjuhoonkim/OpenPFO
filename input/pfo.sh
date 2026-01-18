#!/bin/sh

#SBATCH --job-name=pfo
#SBATCH --account=def-jphickey
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

module load python 3.11
module load openfoam/v2312
module load paraview/6.0.0

pfo checkRun --count=10