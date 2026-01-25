# typing
from typing import Any

# classes
from classes.solution import Solution

# constants
from constants.objective import ObjectiveType

# util
from util.get_points import get_point
from util.get_config_objectives import get_config_objectives


def get_solutions(result: Any):
    solutions: list[Solution] = []

    for i in range(len(result.X)):
        objectives = get_config_objectives()

        point = get_point(coordinates=result.X[i])
        for j, objective_value in enumerate(result.F[i]):
            config_objective = objectives[j]
            if config_objective.get_type() == ObjectiveType.MAXIMIZE:
                objectives[j].set_value(-1 * objective_value)
            else:
                objectives[j].set_value(objective_value)

        solution = Solution(point=point, objectives=objectives)
        solutions.append(solution)

    return solutions
