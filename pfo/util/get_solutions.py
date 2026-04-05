# typing
from typing import Any

# classes
from classes.solution import Solution

# constants
from constants.objective import ObjectiveType

# util
from util.get_points import get_point
from util.get_config_objectives import get_config_objectives

config_objectives = get_config_objectives()


def get_solutions(result: Any):
    solutions: list[Solution] = []

    # if this is a single-objective problem, result will simply return one best
    # point, for multi-objective problems, result will be an list of
    # non-dominated solutions
    if len(config_objectives) == 1:
        point = get_point(coordinates=result.X)
        objective = get_config_objectives()[0]
        objective_value = result.F[0]
        if objective.get_type() == ObjectiveType.MAXIMIZE:
            objective.set_value(-1 * objective_value)
        else:
            objective.set_value(objective_value)

        solution = Solution(point=point, objectives=[objective])
        solutions.append(solution)
    else:
        for i in range(len(result.X)):
            point = get_point(coordinates=result.X[i])
            objectives = get_config_objectives()
            for j, objective_value in enumerate(result.F[i]):
                objective = objectives[j]
                if objective.get_type() == ObjectiveType.MAXIMIZE:
                    objectives[j].set_value(-1 * objective_value)
                else:
                    objectives[j].set_value(objective_value)

            solution = Solution(point=point, objectives=objectives)
            solutions.append(solution)

    return solutions
