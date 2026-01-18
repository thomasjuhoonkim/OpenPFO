# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output
from commands.check_config import check_config

# classes
from classes.problem import OpenPFOProblem

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_initial_objectives import get_initial_objectives
from util.get_logger import get_logger

# user
from create_algorithm import create_algorithm

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2

# ==============================================================================

logger = get_logger()


def doe(
    cleanup: Annotated[bool, typer.Option(help="Run cleanup after each job")] = True,
):
    # pre-run checks
    check_output()
    check_config()
