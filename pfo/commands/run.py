# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.problem import OpenPFOProblem
from classes.progress import Progress

# util
from util.get_config_parameters import get_config_parameters
from util.get_config_objectives import get_config_objectives
from util.format_solutions import format_solutions
from util.get_solutions import get_solutions
from util.get_logger import get_logger

# datetime
from datetime import datetime

# algorithm
from A_create_algorithm import create_algorithm

logger = get_logger()


def run(
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
    resume: Annotated[
        bool, typer.Option(help="Resume progress from an existing run")
    ] = False,
):
    # pre-run checks
    if not resume:
        check_output()
    check_config()

    # progress
    progress = Progress(resume=resume)

    # start time and/or resume time
    start_time = None
    if resume:
        start_time = progress.get_start_time()
        resume_time = datetime.now()
        logger.info(f"Original start time: {start_time}")
        logger.info(f"Resume time: {resume_time}")
    else:
        start_time = datetime.now()
        logger.info(f"Start time: {start_time}")
        progress.save_start_time(start_time=start_time)

    # pymoo
    parameters = get_config_parameters()
    objectives = get_config_objectives()
    problem = OpenPFOProblem(
        should_execute_cleanup=cleanup,
        parameters=parameters,
        objectives=objectives,
        progress=progress,
    )
    algorithm = create_algorithm(problem=problem)

    # run
    result = algorithm.run()

    # map solution
    solutions = get_solutions(result=result)

    # solution
    logger.info("Final result:")
    logger.info(format_solutions(solutions=solutions))
    progress.save_solutions(solutions=solutions)

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
