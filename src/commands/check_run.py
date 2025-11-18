# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output

# classes
from classes.job import Job

# util
from util.get_random_points import get_random_points


def check_run(
    count: Annotated[
        int, typer.Option(help="The number of random points to generate")
    ] = 1,
    objectives: Annotated[
        bool, typer.Option(help="Run asset extraction after each job")
    ] = True,
    assets: Annotated[
        bool, typer.Option(help="Run asset extraction after each job")
    ] = True,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_output()

    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-run-{i}"
        job = Job(job_id=job_id, point=point)

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
