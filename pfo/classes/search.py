# datetime
from datetime import datetime

# threading
import threading

# concurrent
import concurrent.futures

# classes
from classes.objective import Objective
from classes.progress import Progress
from classes.point import Point
from classes.job import Job

# util
from util.get_logger import get_logger
from util.get_config import get_config

logger = get_logger()
config = get_config()


class Search:
    def __init__(self, id: str, points: list["Point"], progress: "Progress"):
        self._id = id
        self._points = points
        self._progress = progress

        self._jobs: list["Job"] = []
        self._job_counter = 0
        self._indices_by_job_id: dict[str, int] = {}
        self._objectives_per_job: list[list[Objective]] = [
            None for _ in range(len(points))
        ]

    def _generate_job_id(self):
        job_index = self._job_counter
        self._job_counter += 1
        return f"{self._id}-job-{job_index}"

    def get_id(self):
        return self._id

    def get_jobs(self):
        return self._jobs

    def create_jobs(self):
        for i, point in enumerate(self._points):
            # because pymoo is fully reproducible, ceteris paribus, each job id yields the same grid point
            job_id = self._generate_job_id()

            # recover or create job
            job = None
            cached_job = self._progress.get_job(job_id=job_id)
            if cached_job is not None:
                job = cached_job
            else:
                point.set_job_id(job_id=job_id)
                job = Job(
                    id=job_id,
                    search_id=self._id,
                    point=point,
                    progress=self._progress,
                )
                job.prepare_job()

            self._jobs.append(job)
            self._indices_by_job_id[job.get_id()] = i

        self._progress.save_search(self)

    def run_all(self, should_execute_cleanup=True):
        lock = threading.Lock()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=config["compute"]["max_job_workers"]
        ) as executor:
            jobs_by_future = {
                executor.submit(
                    job.dispatch,
                    should_execute_cleanup=should_execute_cleanup,
                    lock=lock,
                ): job
                for job in self._jobs
            }

            for future in concurrent.futures.as_completed(jobs_by_future):
                job = jobs_by_future[future]
                try:
                    index = self._indices_by_job_id[job.get_id()]
                    self._objectives_per_job[index] = job.get_objectives()
                    logger.info(f"Job {job.get_id()} completed successfully")
                except BaseException:
                    logger.exception(
                        f"An exception occured while running job {job.get_id()}"
                    )

        self._progress.save_search(self)

        logger.info(f"Search {self._id} complete")

    def get_objectives_per_job(self):
        return self._objectives_per_job

    def serialize(self):
        earliest_start_times = sorted([job.get_start_time() for job in self._jobs])
        earliest_start_time = (
            earliest_start_times[0] if len(earliest_start_times) else datetime.now()
        )
        latest_end_times = sorted(
            [job.get_end_time() for job in self._jobs], reverse=True
        )
        latest_end_time = (
            latest_end_times[0] if len(latest_end_times) else datetime.now()
        )
        return {
            "id": self._id,
            "jobs": [job.get_id() for job in self._jobs],
            "points": [point.serialize() for point in self._points],
            "startTime": earliest_start_time.isoformat(),
            "endTime": latest_end_time.isoformat(),
        }
