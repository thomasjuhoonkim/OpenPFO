# datetime
from datetime import datetime

# system
import os

# typer
import typer
from typing_extensions import Annotated

# classes
from classes.job import Job
from classes.point import Point
from classes.progress import Progress

# constants
from constants.path import OUTPUT_CASES_DIRECTORY

# commands
from commands.check_config import check_config
from commands.check_output import check_output

# util
from util.get_logger import get_logger

logger = get_logger()


# NOTE: needs refactoring to support both existing and not existing runs
def check_extraction(
    existing: Annotated[
        bool, typer.Option(help="Run the check on existing output data")
    ] = True,
    solve: Annotated[bool, typer.Option(help="Run the solver on each job")] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_config()
    if not existing:
        check_output()

    # progress
    progress = Progress()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # jobs
    job_ids = os.listdir(OUTPUT_CASES_DIRECTORY)
    job_ids.sort()
    for job_id in job_ids:
        job = Job(id=job_id, point=Point(variables=[]), progress=progress)

        job.dispatch(
            should_run_checks=False,
            should_create_geometry=not existing,
            should_modify_case=not existing,
            should_create_mesh=not existing,
            should_execute_solver=solve,
            should_extract_objectives=solve,
            should_extract_assets=True,
            should_execute_cleanup=cleanup,
        )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
