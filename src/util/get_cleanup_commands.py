from util.get_config import get_config


config = get_config()

IS_HPC = config["compute"]["hpc"]
PROCESSORS = config["compute"]["processors"]


def get_cleanup_commands(case_directory: str):
    commands = []

    hpc_commands = [
        f'mpirun -np {PROCESSORS} drm --match "^processor.*" {case_directory}',
        f'mpirun -np {PROCESSORS} drm --match "^dynamicCode$" {case_directory}',
        f'mpirun -np {PROCESSORS} drm --match "^VTK$" {case_directory}',
        f'mpirun -np {PROCESSORS} drm --match "^polyMesh$" {case_directory}/constant',
        f'mpirun -np {PROCESSORS} drm --match "[1-9]*" {case_directory}',
        f'mpirun -np {PROCESSORS} drm --match "[0-9]*\.[0-9]*" {case_directory}',
    ]
    if IS_HPC:
        commands.extend(hpc_commands)

    pyfoam_commands = [
        f"pyFoamClearCase.py {case_directory}",
    ]
    commands.extend(pyfoam_commands)

    return commands
