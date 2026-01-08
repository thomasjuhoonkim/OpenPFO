# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output

# classes
from classes.job import Job

# util
from util.get_random_points import get_random_points


def check_cases(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    visualize: Annotated[
        bool, typer.Option(help="Whether to visualize the geometry using pyvista")
    ] = False,
):
    # pre-run checks
    check_output()

    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-cases-{i}"
        job = Job(job_id=job_id, point=point)

        job.prepare_job()
        job.dispatch(
            should_create_geometry=True,
            should_modify_case=True,
            should_create_mesh=False,
            should_execute_solver=False,
            should_extract_objectives=False,
            should_extract_assets=False,
            should_execute_cleanup=False,
        )
        if visualize:
            job.visualize_geometry()
