from typing import Any

from pymoo.algorithms.moo.nsga2 import NSGA2


def create_algorithm(problem: Any):
    algorithm = None

    algorithm = NSGA2(pop_size=2)
    algorithm.setup(
        problem=problem,
        termination=("n_gen", 2),
        seed=1,
        verbose=True,
        # save_history=True,
    )

    return algorithm
