# OpenPFO

## Usage

OpenPFO requires Python 3.11

### Install

To start using OpenPFO, install the software

```
pip install -e .
```

### Inputs and Configuration

OpenPFO runs on three sets of input:

1. `input/model`: The model to use to generate geometries in the design space
2. `input/case_template`: The OpenFOAM case template for all points in the design space
3. `input/objective_function.py`: The objective function for the optimization

OpenPFO also requires a configuration for your optimization case under `config.toml`. The configuration file defines:

- Geometric modeler: The type of modeler to use in the optimization case
- Model interface path: The path to the model interface (if required)
- Parameters: Parameter charactaristics in the design space
- ...

### Commands

Below are the high-level overview of the commands available in OpenPFO, use `[command] --help` for more detailed information.

- `pfo version`: The current version of OpenPFO

- `pfo resetConfig`: Resets the configuration file in `config.toml` back to original settings. (WARNING: Your progress will be lost)
- `pfo createGeometry`: Resets the create_geometry function in `src/create_geometry.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetModifyCase`: Resets the modify_case function in `src/modify_case.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetCreateMesh`: Resets the create_mesh function in `src/create_mesh.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetExecuteSolver`: Resets the execute_solver function in `src/execute_solver.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetExtractObjectives`: Resets the extract_objectives function in `src/extract_objectives.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetExtractAssets`: Resets the extract_assets function in `src/extract_assets.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetExecuteCleanup`: Resets the execute_cleanup function in `src/execute_cleanup.py` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetCaseTemplate`: Resets the case template directory in `input/case_template` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetInput`: Resets the input directory in `input/` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetOutput`: Resets the output directory in `output/` back to original settings. (WARNING: Your progress will be lost)
- `pfo resetAll`: Resets the entire optimization case including the configuration, case template, objective function, and output directory. (WARNING: Your progress will be lost)

- `pfo checkFiles`: Check the existence of optimization files including the config file, model, case template, and the objective function.
- `pfo checkConfig`: Check the validity of the configuration file in `config.toml`.
- `pfo checkModel`: Check the interfacing between the model file and the model API.
- `pfo checkCase`: Check the validity of the optimization case including the optimization algorithm and the objective function.
- `pfo checkMeshes`: Check the validity of the mesh template by generating random points in the design space.
- `pfo checkRun`: Check the validity of the full run including `modify_case`, `extract_assets`, and `extract_objectives` by generating random points in the design space.

- `pfo run`: Run the optimization case.

- `pfo openReport`: Open the report of the optimization results.

## Getting Started (Development)

### Python

OpenPFO requires Python 3.11.

### Virtual Environment & Dependencies

To start using OpenPFO, create a virtual environment

```
python3 -m venv .venv
```

Activate the virtual environment

```
source .venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Finally, when you are finished, run to close the virtual environment.

```
deactivate
```

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
