# system
import sys
import os

# json
import json

# typing
from typing import TYPE_CHECKING

# datetime
from datetime import datetime

# util
from util.validate_results import validate_results
from util.get_serialized_job import get_serialized_job


# classes
if TYPE_CHECKING:
    from classes.job import Job
    from classes.search import Search
    from classes.solution import Solution

# constants
from constants.path import OUTPUT_RESULTS_JSON

# util
from util.get_serialized_objective import get_serialized_objective
from util.get_serialized_parameter import get_serialized_parameter
from util.get_logger import get_logger
from util.get_config import get_config

config = get_config()
logger = get_logger()


class Progress:
    def __init__(self, results_json_filepath=None):
        if results_json_filepath:
            if not os.path.isfile(OUTPUT_RESULTS_JSON):
                logger.error(f"{OUTPUT_RESULTS_JSON} does not exist")
                sys.exit(1)
            logger.info(f"{OUTPUT_RESULTS_JSON} found!")

            with open(results_json_filepath, "r") as json_file:
                self._results = json.load(json_file)

            validate_results(self._results)

            self._start_time = self._results["startTime"]
            self._end_time = self._results["endTime"]
            self._existing_results = True
        else:
            self._results = {
                "config": config,
                "workflow": {"jobs": [], "searches": []},
                "solutions": [],
                "executionTimeSeconds": 0,
                "startTime": "",
                "endTime": "",
                "command": " ".join(sys.argv),
            }
            self._start_time = datetime.now()
            self._end_time = datetime.now()
            self._existing_results = False

    def _save(self):
        with open(OUTPUT_RESULTS_JSON, "w") as results_json:
            json.dump(self._results, results_json, indent=2)

        logger.debug(f"Results saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_job(self, job: "Job"):
        job_result = get_serialized_job(job)

        job_index = next(
            (
                i
                for i, _job in enumerate(self._results["workflow"]["jobs"])
                if _job["id"] == job.get_id()
            ),
            None,
        )

        if job_index is not None:
            self._results["workflow"]["jobs"][job_index] = job_result
        else:
            self._results["workflow"]["jobs"].append(job_result)

        self._save()

        logger.debug(f"Job saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_search(self, search: "Search"):
        search_result = {}

        search_result["id"] = search.get_id()
        search_result["jobs"] = [j.get_id() for j in search.get_jobs()]

        search_index = next(
            (
                i
                for i, _search in enumerate(self._results["workflow"]["searches"])
                if _search["id"] == search.get_id()
            ),
            None,
        )

        if search_index is not None:
            self._results["workflow"]["searches"][search_index] = search_result
        else:
            self._results["workflow"]["searches"].append(search_result)

        self._save()

        logger.debug(f"Search saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_solutions(self, solutions: list["Solution"]):
        solutions_result = []

        for solution in solutions:
            parameters = []
            objectives = []

            for parameter in solution.get_parameters():
                parameters.append(get_serialized_parameter(parameter=parameter))

            for objective in solution.get_objectives():
                objectives.append(get_serialized_objective(objective=objective))

            solutions_result.append(
                {"parameters": parameters, "objectives": objectives}
            )

        self._results["solutions"] = solutions_result

        self._save()

        logger.debug(f"Solution saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_start_time(self, start_time: datetime = None):
        if self._existing_results:
            return None

        if start_time is None:
            start_time = datetime.now()
            self._start_time = start_time

        self._results["startTime"] = start_time.isoformat()

        self._save()

        logger.debug(f"Start time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_end_time(self, end_time: datetime = None):
        if end_time is None:
            end_time = datetime.now()
            self._end_time = end_time

        self._results["endTime"] = end_time.isoformat()

        self._save()

        logger.debug(f"End time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_execution_time(self, execution_time: int = None):
        if execution_time is None:
            time_diff = self._end_time - self._start_time
            execution_time = time_diff.total_seconds()

        self._results["executionTimeSeconds"] = execution_time

        self._save()

        logger.debug(f"Execution time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None
