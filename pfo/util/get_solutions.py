# typing
from typing import Any

# classes
from classes.solution import Solution

# constants
from constants.objective import ObjectiveType

# util
from util.get_config_objectives import get_config_objectives
from util.get_config_parameters import get_config_parameters


def get_solutions(result: Any):
    solutions: list[Solution] = []

    for i in range(len(result.X)):
        parameters = get_config_parameters()
        objectives = get_config_objectives()

        for j, parameter_value in enumerate(result.X[i]):
            parameters[j].set_value(parameter_value)
        for j, objective_value in enumerate(result.F[i]):
            config_objective = objectives[j]
            if config_objective.get_type() == ObjectiveType.MAXIMIZE:
                objectives[j].set_value(-1 * objective_value)
            else:
                objectives[j].set_value(objective_value)

        solution = Solution(parameters=parameters, objectives=objectives)
        solutions.append(solution)

    return solutions
