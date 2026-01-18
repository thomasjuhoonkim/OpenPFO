# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.job import Job

# util
from util.get_random_points import get_random_points


def check_geometries(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    visualize: Annotated[
        bool, typer.Option(help="Whether to visualize the geometry using pyvista")
    ] = False,
):
    # pre-run checks
    check_output()
    check_config()

    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-geometries-{i}"
        job = Job(job_id=job_id, point=point)

        job.prepare_job(should_create_case_directory=False)
        job.dispatch(
            should_create_geometry=True,
            should_modify_case=False,
            should_create_mesh=False,
            should_execute_solver=False,
            should_extract_objectives=False,
            should_extract_assets=False,
            should_execute_cleanup=False,
        )
        if visualize:
            job.visualize_geometry()
