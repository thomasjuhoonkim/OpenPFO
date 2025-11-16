# numpy
import numpy as np

# queue
import collections

# typing
from typing import Deque

# constants
from constants.modeler import AbstractModeler

# classes
from classes.job import Job
from classes.point import Point

# util
from util.get_logger import get_logger

# ==============================================================================

logger = get_logger()


class Search:
    def __init__(
        self,
        search_id: str,
        grid_points: list[Point],
        modeler: AbstractModeler,
    ):
        self._search_id = search_id
        self._grid_points = grid_points
        self._modeler = modeler

        self._jobs: list[Job] = []
        self._job_queue: Deque[Job] = collections.deque()
        self._job_count = 0
        self._all_objectives_values: list[list[np.float64]] = []

    def _generate_job_id(self):
        id = self._job_count
        self._job_count += 1
        return f"{self._search_id}-job-{id}"

    def _create_single_job(self, point: Point):
        """
        Generate job for grid point
        """

        job_id = self._generate_job_id()
        job = Job(job_id=job_id, point=point, modeler=self._modeler)
        job.prepare_geometry()
        job.prepare_case()
        job.prepare_assets()

        return job

    def create_all_jobs(self):
        """
        Generate jobs for all grid points
        """

        for grid_point in self._grid_points:
            job = self._create_single_job(point=grid_point)

            self._jobs.append(job)
            self._job_queue.append(job)

    def get_search_id(self):
        return self._search_id

    def get_jobs(self):
        return self._jobs

    def get_all_objective_values(self):
        return self._all_objectives_values

    def run(self):
        while len(self._job_queue) > 0:
            job = self._job_queue.popleft()
            job.dispatch()

            objective_values = job.get_objective_values()
            self._all_objectives_values.append(objective_values)
