# numpy
import numpy as np

# pymoo
from pymoo.core.problem import Problem

# constants
from constants.objective import ObjectiveType

# classes
from classes.point import Point
from classes.search import Search
from classes.variable import Variable
from classes.progress import Progress
from classes.objective import Objective
from classes.parameter import Parameter

# util
from util.get_logger import get_logger

logger = get_logger()


class OpenPFOProblem(Problem):
    def __init__(
        self,
        parameters: list["Parameter"],
        objectives: list["Objective"],
        progress: "Progress",
        should_execute_cleanup=True,
    ):
        self._parameters = parameters
        self._objectives = objectives
        self._search_count = 0
        self._progress = progress
        self._should_execute_cleanup = should_execute_cleanup

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

    def _get_grid_points(self, x: list[list[np.float64]]) -> list["Point"]:
        parameters = self._parameters

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

        search = Search(id=search_id, grid_points=grid_points, progress=self._progress)
        search.create_jobs()
        search.run_all(should_execute_cleanup=self._should_execute_cleanup)

        # convert objectives into pymoo objectives
        objectives_per_job = search.get_objectives_per_job()
        job_objective_values = []
        for job_objectives in objectives_per_job:
            objective_values = []
            for objective in job_objectives:
                real_value = None
                if not objective.is_valid():
                    if objective.get_type() == ObjectiveType.MINIMIZE:
                        real_value = np.finfo(np.float64).max
                    else:
                        real_value = np.finfo(np.float64).min
                else:
                    real_value = objective.get_value()
                # pymoo expects minimization for all objectives
                minimized_value = (
                    -1 * real_value
                    if objective.get_type() == ObjectiveType.MAXIMIZE
                    else real_value
                )
                objective_values.append(minimized_value)
            job_objective_values.append(objective_values)

        # objectives - transpose into list of objective values per objectives
        # N = number of objectives
        # M = number of jobs
        # N Rows x M columns
        objective_values_per_objective = list(zip(*job_objective_values))
        out["F"] = objective_values_per_objective
