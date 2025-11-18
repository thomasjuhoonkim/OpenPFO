# system
import subprocess

# classes
from classes.functions import ExecuteCleanupParameters


def execute_cleanup(execute_cleanup_parameters: ExecuteCleanupParameters) -> None:
    """
    The execute_cleanup function used to clean up solver artifacts after each job.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_cleanup_parameters.output_case_directory
    logger = execute_cleanup_parameters.logger
    commands = [
        # f'mpirun -np {PROCESSORS} drm --match "^processor.*" {case_directory}',
        # f'mpirun -np {PROCESSORS} drm --match "^dynamicCode$" {case_directory}',
        # f'mpirun -np {PROCESSORS} drm --match "^VTK$" {case_directory}',
        # f'mpirun -np {PROCESSORS} drm --match "^polyMesh$" {case_directory}/constant',
        # f'mpirun -np {PROCESSORS} drm --match "[1-9]*" {case_directory}',
        # f'mpirun -np {PROCESSORS} drm --match "[0-9]*\.[0-9]*" {case_directory}',
        f"pyFoamClearCase.py {case_directory}",
    ]

    for command in commands:
        try:
            subprocess.run(
                command.split(" "), capture_output=True, text=True, check=True
            )
            logger.info(f"Successfully cleaned up solver artifacts in {case_directory}")
        except subprocess.CalledProcessError as error:
            logger.error(f"{command} failed")
            logger.error(f"\n{error.stderr}")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
