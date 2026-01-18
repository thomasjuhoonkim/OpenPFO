# classes
from classes.objective import Objective
from classes.parameter import Parameter


class Solution:
    def __init__(self, parameters: list[Parameter], objectives: list[Objective]):
        self._parameters = parameters
        self._objectives = objectives

    def get_parameters(self):
        return self._parameters

    def get_objectives(self):
        return self._objectives

    def get_solution_representation(self):
        parameters = [
            f"{parameter.get_name()} = {parameter.get_value()}"
            for parameter in self._parameters
        ]
        objectives = [
            f"{objective.get_name()} = {objective.get_value()}"
            for objective in self._objectives
        ]
        parameters_joined = "\n".join(parameters)
        objectives_joined = "\n".join(objectives)
        return f"PARAMETERS\n{parameters_joined}\nOBJECTIVES\n{objectives_joined}"
