# datetime
from datetime import datetime

# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.job import Job

# util
from util.get_logger import get_logger
from util.get_progress import get_progress
from util.get_random_points import get_random_points

logger = get_logger()
progress = get_progress()


def check_prepare(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
):
    # pre-run checks
    check_output()
    check_config()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # jobs
    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-meshes-{i}"
        job = Job(job_id=job_id, point=point)
        job.prepare_job()

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)

    # execution time
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time.total_seconds()} s")
    progress.save_execution_time(execution_time.total_seconds())
