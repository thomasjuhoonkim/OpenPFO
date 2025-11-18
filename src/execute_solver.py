# classes
from classes.functions import ExecuteSolverParameters

# util
from util.get_config import get_config

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


config = get_config()

PROCESSORS = config["compute"]["processors"]


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
) -> None:
    """
    The execute_solver function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_solver_parameters.output_case_directory
    logger = execute_solver_parameters.logger
    commands = [
        f"mpirun -np {PROCESSORS} redistributePar -parallel -decompose -overwrite -case {case_directory}",
        f"mpirun -np {PROCESSORS} simpleFoam -parallel -case {case_directory}",
        f"mpirun -np {PROCESSORS} redistributePar -parallel -reconstruct -latestTime -case {case_directory}",
    ]

    for command in commands:
        runner = BasicRunner(argv=command.split(" "))
        runner.start()
        if not runner.runOK():
            logger.error(f"{command} failed")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
