# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output

# classes
from classes.problem import OpenPFOProblem

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_logger import get_logger
from util.get_objectives import get_objectives

# user
from create_algorithm import create_algorithm

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2

# ==============================================================================

logger = get_logger()


def run(
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_output()
    # check_model()

    # configure initial parameters
    parameters = get_initial_parameters()
    objectives = get_objectives()

    # problem
    problem = OpenPFOProblem(
        parameters=parameters, objectives=objectives, should_execute_cleanup=cleanup
    )
    algorithm: NSGA2 = create_algorithm(problem)

    while algorithm.has_next():
        logger.info(f"n_gen: {algorithm.n_gen}")
        logger.info(f"data: {algorithm.data}")
        algorithm.next()

    result = algorithm.result()
    logger.info(f"Execution time: {result.exec_time} s")
    logger.info("Final result:")
    for i, x in enumerate(result.X):
        logger.info(f"{parameters[i].get_name()} = {x}")
