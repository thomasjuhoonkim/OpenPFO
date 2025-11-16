# typer
from typing_extensions import Annotated
import typer

# commands
from commands.check_model import check_model
from commands.check_output import check_output

# classes
from classes.job import Job

# util
from util.get_modeler import get_modeler
from create_run import create_run
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
    check_model()

    modeler = get_modeler()
    grid_points = get_random_points(count=int(count))
    for i, point in enumerate(grid_points):
        job_id = f"check-run-{i}"
        job = Job(job_id=job_id, point=point, modeler=modeler)

        job.prepare_assets()
        job.prepare_geometry()
        job.prepare_case()
        job.dispatch(
            create_commands=create_run,
            should_cleanup=cleanup,
            should_extract_assets=assets,
            should_extract_objectives=objectives,
        )
