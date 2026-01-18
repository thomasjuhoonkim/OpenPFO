# classes
from classes.functions import ExecuteSolverParameters, ExecuteSolverReturn

# util
from util.get_config import get_config

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


config = get_config()

PROCESSORS = config["compute"]["processors"]


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
) -> ExecuteSolverReturn:
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

    run_ok = True
    for command in commands:
        runner = BasicRunner(argv=command.split(" "))
        runner.start()
        if not runner.runOK():
            run_ok = False
            logger.error(f"{command} failed")

    EXECUTE_SOLVER_RETURN = ExecuteSolverReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_SOLVER_RETURN
