#!/bin/sh

source .venv/bin/activate

pip install -r requirements-hpc.txt

pip install -e .

export SQUEUE_FORMAT='%i","%j","%t","%M","%L","%D","%C","%m","%b","%R'