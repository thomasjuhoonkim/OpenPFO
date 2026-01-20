# numpy
import numpy as np

# classes
from classes.job import Job
from classes.point import Point
from classes.progress import Progress

# util
from util.get_logger import get_logger

logger = get_logger()


class Search:
    def __init__(self, id: str, grid_points: list["Point"], progress: "Progress"):
        self._id = id
        self._grid_points = grid_points
        self._progress = progress

        self._jobs: list["Job"] = []
        self._job_counter = 0
        self._all_objectives_values: list[list[np.float64]] = []

        progress.save_search(self)

    def _generate_job_id(self):
        job_id = self._job_counter
        self._job_counter += 1
        return f"{self._id}-job-{job_id}"

    def get_id(self):
        return self._id

    def get_jobs(self):
        return self._jobs

    def get_all_objective_values(self):
        return self._all_objectives_values

    def run(self, should_execute_cleanup=True):
        for grid_point in self._grid_points:
            # because pymoo is fully reproducible, ceteris paribus, each job id yields the same grid point
            job_id = self._generate_job_id()

            # recover or create job
            job = None
            cached_job = self._progress.get_job(job_id=job_id)
            if cached_job is not None:
                job = cached_job
            else:
                job = Job(id=job_id, point=grid_point, progress=self._progress)
                job.prepare_job()

            self._jobs.append(job)
            self._progress.save_search(self)

            # run job
            job.dispatch(should_execute_cleanup=should_execute_cleanup)

            # objectives
            objectives = job.get_objectives()
            objective_values = [objective.get_pymoo_value() for objective in objectives]
            self._all_objectives_values.append(objective_values)

        logger.info(f"Search {self._id} complete")

    def serialize(self):
        return {"id": self._id, "jobs": [job.get_id() for job in self._jobs]}
