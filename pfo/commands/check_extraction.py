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

# constants
from constants.path import OUTPUT_CASES_DIRECTORY

# commands
from commands.check_config import check_config
from commands.check_output import check_output

# util
from util.get_logger import get_logger
from util.get_progress import get_progress

logger = get_logger()
progress = get_progress()


def check_extraction(
    existing: Annotated[
        bool, typer.Option(help="Run the check on existing output data")
    ] = False,
    solve: Annotated[bool, typer.Option(help="Run the solver on each job")] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_config()
    if not existing:
        check_output()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # jobs
    job_ids = os.listdir(OUTPUT_CASES_DIRECTORY)
    job_ids.sort()
    for job_id in job_ids:
        job = Job(job_id=job_id, point=Point(variables=[]))

        job.dispatch(
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

    # execution time
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time.total_seconds()} s")
    progress.save_execution_time(execution_time.total_seconds())
