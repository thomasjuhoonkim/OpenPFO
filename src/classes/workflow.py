# system
import tomllib

from classes.optimizer import Optimizer
from classes.parameter import Parameter
from classes.search import Search
from classes.job import Job

# ==============================================================================

# config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)


class Workflow:
    _count = 0
    _search_queue: list[Search] = []
    _job_queue: list[Job] = []

    def __init__(self, parameters: list[Parameter], optimizer: Optimizer):
        self._parameters = parameters
        self._optimizer = optimizer

        # instantiate initial search
        search_id = self._generate_search_id()
        search = Search(search_id=search_id, parameters=self._parameters)
        search.discretize_parameters()
        search.create_grid_points()
        search.create_all_jobs()

        jobs = search.get_jobs()
        for job in jobs:
            print(job.get_job_id())
            job.visualize_geometry()

    def _generate_search_id(self):
        id = self._count
        self._count += 1
        return f"search-{id}"

    def queue_search(self, search: Search):
        self._search_queue.append(search)
        self._job_queue = self._job_queue + [*search.get_jobs()]

    def get_search_queue(self):
        return self._search_queue

    def get_job_queue(self):
        return self._job_queue
