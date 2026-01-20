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
from classes.progress import Progress

# util
from util.get_logger import get_logger
from util.get_random_points import get_random_points

logger = get_logger()


def check_meshes(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    assets: Annotated[
        bool, typer.Option(help="Run asset extraction after each job")
    ] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = False,
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
    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-meshes-{i}"
        job = Job(id=job_id, point=point, progress=progress)

        job.prepare_job()
        job.dispatch(
            should_create_geometry=True,
            should_modify_case=True,
            should_create_mesh=True,
            should_execute_solver=False,
            should_extract_objectives=False,
            should_extract_assets=assets,
            should_execute_cleanup=cleanup,
        )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
