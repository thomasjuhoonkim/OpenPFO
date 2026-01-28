# system
import sys

# datetime
from datetime import datetime

# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.progress import Progress
from classes.search import Search
from classes.point import Point

# util
from util.get_linear_points import get_linear_points
from util.get_random_points import get_random_points
from util.get_logger import get_logger

logger = get_logger()


def check_geometries(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    random: Annotated[
        bool, typer.Option(help="Randomize points in the design space")
    ] = True,
    visualize: Annotated[
        bool, typer.Option(help="Whether to visualize the geometry using pyvista")
    ] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = False,
):
    # pre-run checks
    check_output()
    check_config()

    if not random and count < 2:
        logger.warning(
            "To run with linear separation, you must ask for 2 or more points of separation"
        )
        sys.exit(1)

    # progress
    progress = Progress()

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

    search = Search(id="check-geometries", points=points, progress=progress)
    search.create_jobs()
    search.run_all(
        should_run_checks=True,
        should_run_prepare=True,
        should_run_geometry=True,
        should_run_mesh=False,
        should_run_solve=False,
        should_run_objectives=False,
        should_run_cleanup=cleanup,
    )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)

    # visualize
    if visualize:
        jobs = search.get_jobs()
        for job in jobs:
            job.visualize_geometry()
