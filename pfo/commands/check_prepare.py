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
from classes.point import Point
from classes.progress import Progress

# util
from util.get_logger import get_logger

logger = get_logger()


def check_prepare(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
):
    # pre-run checks
    check_output()
    check_config()

    # progress
    progress = Progress()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # jobs
    points = [Point(variables=[]) for _ in range(count)]
    for i, point in enumerate(points):
        job_id = f"check-meshes-job-{i}"
        job = Job(id=job_id, point=point, progress=progress)
        job.prepare_job()

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
