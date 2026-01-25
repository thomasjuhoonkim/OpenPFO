# classes
from classes.point import Point
from classes.objective import Objective


class Solution:
    def __init__(self, point: Point, objectives: list[Objective]):
        self._point = point
        self._objectives = objectives

    def get_point(self):
        return self._point

    def get_objectives(self):
        return self._objectives

    def get_solution_representation(self):
        variables = [
            f"{variable.get_name()} = {variable.get_value()}"
            for variable in self._point.get_variables()
        ]
        objectives = [
            f"{objective.get_name()} = {objective.get_value()}"
            for objective in self._objectives
        ]
        variables_joined = "\n".join(variables)
        objectives_joined = "\n".join(objectives)
        return f"VARIABLES\n{variables_joined}\nOBJECTIVES\n{objectives_joined}"
