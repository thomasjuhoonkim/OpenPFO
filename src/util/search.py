# system
import sys

# geometry
import itertools

# logging
import logging
from logger.logger import LOGGER_NAME

# utils
from util.job import Job
from util.parameter import Parameter
from util.point import Point
from util.variable import Variable

# ==============================================================================

# logging
logger = logging.getLogger(LOGGER_NAME)


class Search:
    _matrix: list[list[float]] = []
    _combinations: list[list[float]] = []
    _jobs: list[Job] = []

    def __init__(self, search_id: str, parameters: list[Parameter]):
        self._count = 0
        self._search_id = search_id
        self._parameters = parameters

    def _generate_job_id(self):
        id = self._count
        self._count += 1
        return f"{self._search_id}-job-{id}"

    def _add_job(self, job: Job):
        self._jobs.append(job)

    def _discretize(self):
        for parameter in self._parameters:
            name = parameter.get_name()
            diff = abs(parameter.get_max() - parameter.get_min())
            grid_separations = parameter.get_grid_points() - 1

            # this should arguably be moved into a OpenPFO setup checking script
            if grid_separations < 1:
                logger.error(f"Parameter '{name}' must have more than 2 grid points")
                sys.exit(1)

            delta = diff / grid_separations
            steps = [
                parameter.get_min() + delta * n for n in range(grid_separations + 1)
            ]
            self._matrix.append(steps)
        logger.info(f"Successfully discretized domain for {self._search_id}")

    def _create_combinations(self):
        self._combinations = list(itertools.product(*self._matrix))
        logger.info(
            f"Successfully created grid point combinations for {self._search_id}"
        )

    def _create_single_job(self, point: Point):
        # 1. generate job id
        # 2. generate geometry for grid point
        # 3. create OpenFOAM case for grid point
        # 4. encode job with case and geometry
        # 5. return job

        job_id = self._generate_job_id()
        job = Job(job_id=job_id, point=point)
        job.generate_geometry()

        return job

    def create_all_jobs(self):
        # 1. discretize domain into grid
        # 2. create grid points from parameter combinations
        # 3. create job for each grid point
        self._discretize()
        self._create_combinations()

        for combination in self._combinations:
            variables = []
            for i, value in enumerate(combination):
                name = self._parameters[i].get_name()
                cell = self._parameters[i].get_cell()
                variable = Variable(name=name, cell=cell, value=value)
                variables.append(variable)

            point = Point(variables)
            job = self._create_single_job(point)

            self._add_job(job)

        # for i in range(len(combinations)):
        # filepath = f"output/geometries/{i}.stl"
        # mesh = pv.read(filepath)
        # mesh.plot()

    def get_search_id(self):
        return self._search_id

    def get_parameters(self):
        return self._parameters

    def get_jobs(self):
        return self._jobs
