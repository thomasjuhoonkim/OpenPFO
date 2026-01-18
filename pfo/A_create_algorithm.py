# typing
from typing import Any

# pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2

# util
from util.get_config import get_config

config = get_config()


def create_algorithm(problem: Any):
    algorithm = None

    algorithm = NSGA2(pop_size=10)
    algorithm.setup(
        problem=problem,
        termination=("n_gen", 10),
        seed=config["optimizer"]["seed"],
        verbose=True,
        save_history=True,
    )

    return algorithm
