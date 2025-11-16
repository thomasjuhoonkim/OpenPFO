from util.get_config import get_config


config = get_config()

PROCESSORS = config["compute"]["processors"]


def create_commands(case_directory):
    """
    Returns list of OpenFOAM commands to run.

    All commands must be separated with a single space. `case_directory` is provided.

    NOTE: This function MUST return the `commands` list.

    NOTE: All case data is deleted after each job automatically. You do not need to specify a clean command
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    commands = [
        f"blockMesh -case {case_directory}",
        f"surfaceFeatureExtract -case {case_directory}",
        f"mpirun -np {PROCESSORS} redistributePar -parallel -decompose -overwrite -case {case_directory}",
        f"mpirun -np {PROCESSORS} snappyHexMesh -parallel -overwrite -case {case_directory}",
        f"mpirun -np {PROCESSORS} redistributePar -parallel -reconstruct -overwrite -constant -case {case_directory}",
        f"mpirun -np {PROCESSORS} redistributePar -parallel -decompose -overwrite -case {case_directory}",
        f"mpirun -np {PROCESSORS} simpleFoam -parallel -case {case_directory}",
        f"mpirun -np {PROCESSORS} redistributePar -parallel -reconstruct -latestTime -case {case_directory}",
    ]

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return commands
