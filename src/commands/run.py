# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.problem import OpenPFOProblem

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_initial_objectives import get_initial_objectives
from util.get_progress import get_progress
from util.get_logger import get_logger

# user
from create_algorithm import create_algorithm

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2

# datetime
from datetime import datetime

from util.get_solutions import get_solutions

# ==============================================================================

logger = get_logger()
progress = get_progress()


def run(
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_output()
    check_config()

    # start time
    start_time = datetime.now()
    progress.save_start_time(start_time=start_time)

    # configure initial parameters
    parameters = get_initial_parameters()
    objectives = get_initial_objectives()

    # problem
    problem = OpenPFOProblem(
        parameters=parameters, objectives=objectives, should_execute_cleanup=cleanup
    )
    algorithm: NSGA2 = create_algorithm(problem=problem)

    # run
    result = algorithm.run()

    # map solution
    solutions = get_solutions(result=result)

    # solution
    solution_representations = [
        f"SOLUTION {i}\n{solution.get_solution_representation()}"
        for i, solution in enumerate(solutions)
    ]
    logger.info("Final result:")
    logger.info("\n" + "\n\n".join(solution_representations))
    progress.save_solutions(solutions=solutions)

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)

    # execution time
    logger.info(f"Execution time: {result.exec_time} s")
    progress.save_execution_time(execution_time=result.exec_time)
