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
from util.get_logger import get_logger
from util.get_linear_points import get_linear_points
from util.get_random_points import get_random_points

logger = get_logger()


def check_solver(
    count: Annotated[int, typer.Option(help="The number of points to generate")] = 1,
    random: Annotated[
        bool, typer.Option(help="Randomize points in the design space")
    ] = True,
    cleanup: Annotated[
        bool, typer.Option(help="Whether to run the cleanup step")
    ] = False,
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

    # points
    points: list["Point"] = []
    if random:
        points = get_random_points(count=count)
    else:
        points = get_linear_points(count=count)
    logger.info("Running points:")
    for point in points:
        logger.info(point.get_representation())

    # search
    search = Search(id="check-solver", points=points, progress=progress)
    search.create_jobs()
    search.run_all(
        should_run_checks=True,
        should_run_prepare=True,
        should_run_geometry=True,
        should_run_mesh=True,
        should_run_solve=True,
        should_run_objectives=False,
        should_run_cleanup=cleanup,
    )

    # end time
    end_time = datetime.now()
    logger.info(f"End time: {end_time}")
    progress.save_end_time(end_time=end_time)
