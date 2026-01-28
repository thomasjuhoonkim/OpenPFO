# datetime
from datetime import datetime

# classes
from classes.progress import Progress

# commands
from commands.check_config import check_config

# util
from util.get_logger import get_logger

logger = get_logger()


def check_objectives():
    # pre-run checks
    check_config()

    # progress
    progress = Progress()
    progress.recover_progress()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # jobs
    jobs = progress.get_jobs()
    for job in jobs:
        job.dispatch(
            should_run_checks=False,
            should_run_prepare=False,
            should_run_geometry=False,
            should_run_mesh=False,
            should_run_solve=False,
            should_run_objectives=True,
            should_run_cleanup=False,
        )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
