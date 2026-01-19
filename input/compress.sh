#!/bin/sh

#SBATCH --job-name=compress
#SBATCH --account=def-jphickey
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=8G
#SBATCH --output=compress
#SBATCH --open-mode=append

tar -vc --use-compress-program="pigz -p 32" -f output.tar.gz output