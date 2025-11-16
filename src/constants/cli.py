import typer

from constants.modeler import EModeler
from constants.optimizer import EOptimizer

OPTIMIZER_ARGUMENT = typer.Argument(
    EOptimizer.NO_OPTIMIZER, help="The type of optimization algorithm to use"
)


MODELER_ARGUMENT = typer.Argument(EModeler.FREECAD, help="The type of modeler to use")
