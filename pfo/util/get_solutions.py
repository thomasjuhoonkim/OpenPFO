# typing
from typing import Any

# classes
from classes.solution import Solution

# util
from util.get_config_objectives import get_config_objectives
from util.get_config_parameters import get_config_parameters


def get_solutions(result: Any):
    solutions: list[Solution] = []

    for individual in result.pop:
        parameters = get_config_parameters()
        objectives = get_config_objectives()

        for j, parameter_value in enumerate(individual.X):
            parameters[j].set_value(parameter_value)
        for j, objective_value in enumerate(individual.F):
            objectives[j].set_value(objective_value)

        solution = Solution(parameters=parameters, objectives=objectives)
        solutions.append(solution)

    return solutions
