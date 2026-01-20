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


def check_run(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    objectives: Annotated[
        bool, typer.Option(help="Extract objectives after each job")
    ] = True,
    assets: Annotated[
        bool, typer.Option(help="Run asset extraction after each job")
    ] = True,
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

    # jobs
    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-run-{i}"
        job = None
        cached_job = progress.get_job(job_id=job_id)
        if cached_job is not None:
            job = cached_job
        else:
            job = Job(id=job_id, point=point, progress=progress)
            job.prepare_job()

        job.dispatch(
            should_create_geometry=True,
            should_modify_case=True,
            should_create_mesh=True,
            should_execute_solver=True,
            should_extract_objectives=objectives,
            should_extract_assets=assets,
            should_execute_cleanup=cleanup,
        )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
