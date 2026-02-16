# typing
from typing import Any

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2


def optimizer(problem: Any):
    algorithm = NSGA2(pop_size=30)
    algorithm.setup(
        problem=problem,
        termination=("n_gen", 20),
        seed=1,
        verbose=True,
        save_history=True,
    )

    return algorithm
