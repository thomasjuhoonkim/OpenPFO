# numpy
import numpy as np

# queue
import collections

# typing
from typing import Deque

# classes
from classes.job import Job
from classes.point import Point

# util
from util.get_logger import get_logger
from util.get_progress import get_progress

# ==============================================================================

logger = get_logger()
progress = get_progress()


class Search:
    def __init__(self, search_id: str, grid_points: list[Point]):
        self._search_id = search_id
        self._grid_points = grid_points

        self._jobs: list[Job] = []
        self._job_queue: Deque[Job] = collections.deque()
        self._job_count = 0
        self._all_objectives_values: list[list[np.float64]] = []

        progress.save_search(self)

    def _generate_job_id(self):
        id = self._job_count
        self._job_count += 1
        return f"{self._search_id}-job-{id}"

    def create_jobs(self):
        for grid_point in self._grid_points:
            job_id = self._generate_job_id()
            job = Job(job_id=job_id, point=grid_point)
            job.prepare_job()

            self._jobs.append(job)
            self._job_queue.append(job)

        progress.save_search(self)

    def get_id(self):
        return self._search_id

    def get_jobs(self):
        return self._jobs

    def get_all_objective_values(self):
        return self._all_objectives_values

    def run(self, should_execute_cleanup=True):
        while len(self._job_queue) > 0:
            job = self._job_queue.popleft()
            job.dispatch(should_execute_cleanup=should_execute_cleanup)

            objectives = job.get_objectives()
            objective_values = [objective.get_pymoo_value() for objective in objectives]
            self._all_objectives_values.append(objective_values)
