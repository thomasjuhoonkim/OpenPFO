# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_output import check_output
from commands.check_config import check_config
from commands.check_foam import check_foam

# classes
from classes.job import Job

# util
from util.get_random_points import get_random_points


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
    check_foam()

    grid_points = get_random_points(count=count)
    for i, point in enumerate(grid_points):
        job_id = f"check-meshes-{i}"
        job = Job(job_id=job_id, point=point)

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
