#!/bin/sh

echo "Deleting processor* directories"
find ./output -type d -name "processor*" -exec rm -rf {} +

echo "Deleting timestep directories"
find ./output -type d -regextype posix-extended -regex "./[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" -exec rm -rf {} +

echo "Deleting VTK directories"
find ./output -type d -name "VTK" -exec rm -rf {} +

pfo resetOutput