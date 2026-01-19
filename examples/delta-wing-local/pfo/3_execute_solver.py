# classes
from classes.functions import ExecuteSolverParameters, ExecuteSolverReturn

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
):
    """
    The execute_solver function is used to create the geometry for each grid
    point in the design space.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_solver_parameters.output_case_directory
    logger = execute_solver_parameters.logger
    processors = execute_solver_parameters.processors

    commands = [
        f"mpirun -np {processors} redistributePar -parallel -decompose -overwrite -case {case_directory}",
        f"mpirun -np {processors} simpleFoam -parallel -case {case_directory}",
        f"mpirun -np {processors} redistributePar -parallel -reconstruct -latestTime -case {case_directory}",
    ]

    for command in commands:
        runner = BasicRunner(argv=command.split(" "))
        runner.start()
        if not runner.runOK():
            logger.error(f"{command} failed")
            raise Exception(f"{command} failed")

    EXECUTE_SOLVER_RETURN = ExecuteSolverReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_SOLVER_RETURN
