from util.search import Search
from util.job import Job


class Workflow:
    def __init__(self):
        self._count = 0
        self._search_queue: list[Search] = []
        self._job_queue: list[Job] = []

    def generate_search_id(self):
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
