# system
import sys

# datetime
from datetime import datetime

# typer
from classes.search import Search
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.point import Point
from classes.progress import Progress

# util
from util.get_logger import get_logger
from util.get_linear_points import get_linear_points
from util.get_random_points import get_random_points

logger = get_logger()


def check_run(
    count: Annotated[int, typer.Option(help="The number of points to generate")] = 1,
    random: Annotated[
        bool, typer.Option(help="Randomize points in the design space")
    ] = True,
    objectives: Annotated[
        bool, typer.Option(help="Whether to run the objectives step")
    ] = True,
    cleanup: Annotated[
        bool, typer.Option(help="Whether to run the cleanup step")
    ] = True,
    resume: Annotated[
        bool, typer.Option(help="Resume progress from an existing run")
    ] = False,
):
    # pre-run checks
    if not resume:
        check_output()
    check_config()

    if not random and count < 2:
        logger.warning(
            "To run with linear separation, you must ask for 2 or more points of separation"
        )
        sys.exit(1)

    # progress
    progress = Progress()
    progress.recover_progress()
    if resume:
        progress.validate_command_match()

    # start time
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    progress.save_start_time(start_time=start_time)

    # points
    points: list["Point"] = []
    if random:
        points = get_random_points(count=count)
    else:
        points = get_linear_points(count=count)
    logger.info("Running points:")
    for point in points:
        logger.info(point.get_representation())

    search = Search(id="check-run", points=points, progress=progress)
    search.create_jobs()
    search.run_all(
        should_run_checks=True,
        should_run_prepare=True,
        should_run_geometry=True,
        should_run_mesh=True,
        should_run_solve=True,
        should_run_objectives=objectives,
        should_run_cleanup=cleanup,
    )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
