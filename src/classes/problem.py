# numpy
import numpy as np

# pymoo
from pymoo.core.problem import Problem

# classes
from classes.point import Point
from classes.search import Search
from classes.variable import Variable
from classes.objective import Objective
from classes.parameter import Parameter

# util
from util.get_initial_parameters import get_initial_parameters
from util.get_logger import get_logger

# ==============================================================================

logger = get_logger()


class OpenPFOProblem(Problem):
    def __init__(
        self,
        parameters: list[Parameter],
        objectives: list[Objective],
    ):
        self._search_count = 0

        lower_bounds = np.array(object=[], dtype=np.float64)
        upper_bounds = np.array(object=[], dtype=np.float64)

        for parameter in parameters:
            lower_bounds = np.append(lower_bounds, parameter.get_min())
            upper_bounds = np.append(upper_bounds, parameter.get_max())

        super().__init__(
            n_var=len(parameters),
            n_obj=len(objectives),
            xl=lower_bounds,
            xu=upper_bounds,
        )

    def _generate_search_id(self):
        id = self._search_count
        self._search_count += 1
        return f"search-{id}"

    def _get_grid_points(self, x: list[list[np.float64]]) -> list[Point]:
        parameters = get_initial_parameters()

        grid_points = []
        for coordinates in x:
            variables = []
            for i, coordinate in enumerate(coordinates):
                variable = Variable(
                    name=parameters[i].get_name(),
                    id=parameters[i].get_id(),
                    value=coordinate,
                )
                variables.append(variable)

            grid_point = Point(variables=variables)
            grid_points.append(grid_point)

        return grid_points

    def _evaluate(self, x, out):
        # x: [N x n_var] where N is the population size and n_var is the number of parameters
        grid_points = self._get_grid_points(x)
        search_id = self._generate_search_id()

        search = Search(search_id=search_id, grid_points=grid_points)
        search.create_jobs()
        search.run()

        objective_values = search.get_all_objective_values()
        out["F"] = objective_values
