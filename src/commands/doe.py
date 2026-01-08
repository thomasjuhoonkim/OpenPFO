# typer
import typer
from typing_extensions import Annotated

# commands
from commands.check_output import check_output

# classes
from classes.problem import OpenPFOProblem

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_logger import get_logger
from util.get_objectives import get_objectives

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
