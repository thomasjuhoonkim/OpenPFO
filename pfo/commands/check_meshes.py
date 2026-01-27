# datetime
from datetime import datetime

# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.point import Point
from classes.search import Search
from classes.progress import Progress

# util
from util.get_logger import get_logger
from util.get_linear_points import get_linear_points
from util.get_random_points import get_random_points

logger = get_logger()


def check_meshes(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    random: Annotated[
        bool, typer.Option(help="Randomize points in the design space")
    ] = True,
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

    # points
    points: list["Point"] = []
    if random:
        points = get_random_points(count=count)
    else:
        points = get_linear_points(count=count)
    logger.info("Running points:")
    for point in points:
        logger.info(point.get_representation())

    search = Search(id="check-meshes", points=points, progress=progress)
    search.create_jobs()
    search.run_all(
        should_run_checks=True,
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
