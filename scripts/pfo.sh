#!/bin/sh

#SBATCH --job-name=pfo
#SBATCH --account=def-jphickey
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --output=OpenPFO.log
#SBATCH --open-mode=append

module load python 3.11
module load openfoam/v2312
module load paraview/6.0.0

pfo checkRun --no-random --count=21