import os
import typer
from typing_extensions import Annotated

from classes.job import Job
from classes.point import Point
from constants.path import OUTPUT_CASES_DIRECTORY
from util.get_logger import get_logger

logger = get_logger()


def check_assets(
    job_id: Annotated[str, typer.Option(help="The path of the case directory")] = "",
):
    job_ids = []
    if job_id:
        job_ids.append(job_id)
    else:
        cases = os.listdir(OUTPUT_CASES_DIRECTORY)
        cases.sort()
        job_ids = cases

    for job_id in job_ids:
        job = Job(job_id=job_id, point=Point(variables=[]))

        job.dispatch(
            should_create_geometry=False,
            should_modify_case=False,
            should_create_mesh=False,
            should_execute_solver=False,
            should_extract_objectives=False,
            should_extract_assets=True,
            should_execute_cleanup=False,
        )
