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

logger = get_logger()


def check_extraction(
    existing: Annotated[
        bool, typer.Option(help="Run the check on existing output data")
    ] = False,
    solve: Annotated[bool, typer.Option(help="Run the solver on each job")] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    check_config()
    if not existing:
        check_output()

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
