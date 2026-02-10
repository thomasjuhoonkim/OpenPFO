# system
import sys
import os

# json
import json

# typing
from typing import TYPE_CHECKING

# datetime
from datetime import datetime

# classes
if TYPE_CHECKING:
    from classes.solution import Solution
    from classes.search import Search
from classes.job import Job

# constants
from constants.path import OUTPUT_RESULTS_JSON

# util
from util.validate_results import validate_results
from util.get_pfo_command import get_pfo_command
from util.get_logger import get_logger
from util.get_config import get_config

config = get_config()
logger = get_logger()


class Progress:
    def __init__(self):
        self._results = {
            "config": config,
            "workflow": {"jobs": [], "searches": []},
            "solutions": [],
            "startTime": "",
            "endTime": "",
            "command": get_pfo_command(sys.argv),
        }
        self._start_time = datetime.now()
        self._end_time = datetime.now()
        self._existing_results = False

        # internal cache
        self._jobs_by_id: dict[str, dict] = {}
        self._searches_by_id: dict[str, dict] = {}

    def validate_command_match(self):
        logger.info("Checking if original command matches current command")
        current_command_set = set(sys.argv)
        if "--resume" in current_command_set:
            current_command_set.remove("--resume")
        results_command = self._results["command"]
        if current_command_set != set(results_command.split(" ")):
            logger.error(
                f"Command used in previous progress ({results_command}) does not match current command ({get_pfo_command(sys.argv)})"
            )
            sys.exit(1)

    def _can_recover_progress(self):
        logger.info("Checking if progress can be recovered")
        validate_results(self._results)
        logger.info("Progress OK")

    def recover_progress(self):
        self._can_recover_progress()

        if os.path.isfile(OUTPUT_RESULTS_JSON):
            with open(OUTPUT_RESULTS_JSON, "r") as json_file:
                self._results = json.load(json_file)

            logger.info(f"{OUTPUT_RESULTS_JSON} found!")

            # internal cache
            self._jobs_by_id: dict[str, dict] = {
                job["id"]: job for job in self._results["workflow"]["jobs"]
            }
            self._searches_by_id: dict[str, dict] = {
                search["id"]: search for search in self._results["workflow"]["searches"]
            }

            start_time = self._results["startTime"]
            end_time = self._results["endTime"]
            self._start_time = (
                datetime.fromisoformat(start_time) if start_time else datetime.now()
            )
            self._end_time = (
                datetime.fromisoformat(end_time) if end_time else datetime.now()
            )
            self._existing_results = True

        logger.info("Progress recovered successfully")

    def _save(self):
        with open(OUTPUT_RESULTS_JSON, "w") as results_json:
            json.dump(self._results, results_json, indent=2)

        logger.debug(f"Results saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_job(self, job: "Job"):
        job_result = job.serialize()

        self._jobs_by_id[job.get_id()] = job_result
        self._results["workflow"]["jobs"] = list(self._jobs_by_id.values())

        self._save()

        logger.debug(f"Job saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_search(self, search: "Search"):
        search_result = search.serialize()

        self._searches_by_id[search.get_id()] = search_result
        self._results["workflow"]["searches"] = list(self._searches_by_id.values())

        self._save()

        logger.debug(f"Search saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_solutions(self, solutions: list["Solution"]):
        solutions_result = []

        for solution in solutions:
            objectives = []

            point = solution.get_point()
            for objective in solution.get_objectives():
                objectives.append(objective.serialize())

            solutions_result.append(
                {"point": point.serialize(), "objectives": objectives}
            )

        self._results["solutions"] = solutions_result

        self._save()

        logger.debug(f"Solution saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_start_time(self, start_time: datetime):
        if self._existing_results:
            return None

        self._results["startTime"] = start_time.isoformat()

        self._save()

        logger.debug(f"Start time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_end_time(self, end_time: datetime):
        self._results["endTime"] = end_time.isoformat()

        self._save()

        logger.debug(f"End time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def get_command(self):
        return self._results["command"]

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_job(self, job_id: str):
        job = self._jobs_by_id.get(job_id, None)
        if job is None:
            return None
        return Job.from_dict(job=job, progress=self)

    def get_jobs(self):
        jobs = list(self._jobs_by_id.values())
        return [Job.from_dict(job=job, progress=self) for job in jobs]
