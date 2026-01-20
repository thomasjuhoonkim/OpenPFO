# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# util
from util.get_config_parameters import get_config_parameters
from util.get_config_objectives import get_config_objectives
from util.get_logger import get_logger

logger = get_logger()


def doe(
    assets: Annotated[
        bool, typer.Option(help="Run asset extraction after each job")
    ] = False,
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_output()
    check_config()
