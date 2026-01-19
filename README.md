# OpenPFO

## Getting Started

Quick setup scripts are provided in `scripts/`.

```
// Local
source scripts/init-local.sh

// HPC
source scripts/init-hpc.sh
```

However, if you prefer to set up the environment yourself, step-by-step instructions are provided below.

### Python

OpenPFO requires Python 3.11.

### Virtual Environment

To start using OpenPFO, create a virtual environment

```
// Python
python3 -m venv .venv

// Virtualenv
virtualenv .venv
```

Activate the virtual environment

```
source .venv/bin/activate
```

### Dependencies

#### Python

Install python dependencies

```
// Local
pip install -r requirements-local.txt

// HPC
pip install -r requirements-hpc.txt
```

#### OpenVSP

Either download OpenVSP from the [official website](https://openvsp.org/download.php) or [build it from source](https://openvsp.org/wiki/doku.php?id=ubuntu_instructions).

> [!NOTE]
> Make sure you have loaded modules `gcc 14` and `swig` before building from source.
> Make sure the flag `-DVSP_USE_SYSTEM_GLEW=false` is set during buildlibs and flags
> `-DVSP_NO_VSPAERO=ON -DVSP_NO_GRAPHICS=ON -DVSP_NO_HELP=ON -DVSP_NO_DOC=ON` are set for build.

#### FreeCAD

To be filled...

### Install

To start using OpenPFO, install the package in editable mode. This is important as OpenPFO is a framework, you design your own implementation.

```
pip install -e .
```

## Usage

### Overview

OpenPFO requires configuration in several locations.

1. `input/`: The input directory where any input files and directories are located.
   1. `input/case_template/`: The OpenFOAM case template.
   2. `input/paraview/`: All paraview macro scripts for `pvbatch`.
   3. `input/model.xyz`: The geometry model.
2. `pfo/0-A.py`: The user-defined functions for OpenPFO.
3. `config.toml`: OpenPFO configuration.

### Inputs

#### Case Template

OpenPFO uses OpenFOAM for CFD solving and optionally meshing. The case template is a single template that all points in the design space inherit. This means your template mesh and solver settings must be compatible with all points in the design space [^1].

### Commands

To be filled...

### SLURM

If you are using `simple-slurm`, make sure your SQUEUE_FORMAT environment variable is valid. If you are unsure about its validity, `simple-slurm` will raise an error. You can also set the variable to `"%i","%j","%t","%M","%L","%D","%C","%m","%b","%R"`, `simple-slurm`'s default value.

## Acknowledgements

### Funding

This project was made possible through the Faculty of Engineering at the University of Waterloo.

### Contributors

- [Thomas Kim](https://www.linkedin.com/in/thomasjuhoonkim) - [thomasjuhoonkim](https://github.com/thomasjuhoonkim) - [thomas.kim@uwaterloo.ca](mailto:thomas.kim@uwaterloo.ca)
- [Kate Armstrong](https://www.linkedin.com/in/katelarmstrong/) - [katelarmstrong](https://github.com/katelarmstrong) - [k24armstrong@uwaterloo.ca](mailto:k24armstrong@uwaterloo.ca)
- [Emma Keeping](https://www.linkedin.com/in/emmaleekeeping/) - [emmaleekeeping](https://github.com/emmaleekeeping) - [ekeeping@uwaterloo.ca](mailto:ekeeping@uwaterloo.ca)

### Advisors

- [Dr. Jean-Pierre Hickey](https://uwaterloo.ca/mechanical-mechatronics-engineering/profile/j6hickey)
- [Dr. Jimmy-John Hoste](https://www.linkedin.com/in/jimmy-john-hoste-17278644/)

### Disclaimer

OpenPFO is part of the University of Waterloo's engineering capstone project courses. Future maintenence of this repository is subject to contributor availability. Contributors are welcome, please reach out to project owners regarding contributing.

[^1]: This is not a strict requirement. OpenPFO will run reasonably well as long as your template mesh and solver settings are compatible with _most_ points in the design space. Localized errors in the design space are simply avoided by the optimization algorithm through infinite objective values and user-defined constraint violations.
