# typing
from typing import Any

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2


def optimizer(problem: Any):
    """
    This function is used to define the `pymoo` optimiztion algorithm.
    """
    algorithm = None

    """ ======================= YOUR CODE BELOW HERE ======================= """

    algorithm = NSGA2(pop_size=30)
    algorithm.setup(
        problem=problem,
        termination=("n_gen", 30),
        seed=1,
        verbose=True,
        save_history=True,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return algorithm
