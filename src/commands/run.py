# commands
from commands.check_model import check_model
from commands.check_output import check_output

# classes
from classes.problem import OpenPFOProblem

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_logger import get_logger
from util.get_objectives import get_objectives
from util.get_optimizer import get_optimizer
from util.get_modeler import get_modeler

# user
from create_algorithm import create_algorithm

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2

# ==============================================================================

logger = get_logger()


def run():
    # pre-run checks
    check_output()
    check_model()

    # configure initial parameters
    parameters = get_initial_parameters()
    objectives = get_objectives()

    # runtime dependencies
    optimizer = get_optimizer()
    modeler = get_modeler()

    # problem
    problem = OpenPFOProblem(
        parameters=parameters, objectives=objectives, modeler=modeler
    )
    algorithm: NSGA2 = create_algorithm(problem)

    while algorithm.has_next():
        logger.info(f"n_gen: {algorithm.n_gen}")
        logger.info(f"data: {algorithm.data}")
        algorithm.next()

    result = algorithm.result()
    logger.info(f"{result.exec_time}")
    logger.info(f"{result.X}")
