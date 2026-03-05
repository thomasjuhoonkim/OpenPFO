#!/bin/sh

#SBATCH --job-name=pfo
#SBATCH --account=def-jphickey
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=cleanup-job.log
#SBATCH --open-mode=append

parallel rm -rf output/check-run-job-0/processor{} ::: $(seq 0 159)