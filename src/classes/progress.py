# json
import json

# typing
from typing import TYPE_CHECKING

# datetime
from datetime import datetime


# classes
if TYPE_CHECKING:
    from classes.job import Job
    from classes.search import Search
    from classes.solution import Solution

# constants
from constants.path import OUTPUT_RESULTS_JSON

# util
from util.get_serialized_objectives import get_serialized_objectives
from util.get_serialized_point import get_serialized_point
from util.get_logger import get_logger
from util.get_config import get_config

config = get_config()
logger = get_logger()


class Progress:
    def __init__(self):
        self._results = {
            "config": config,
            "workflow": {"jobs": [], "searches": []},
            "solutions": {"parameters": [], "objectives": []},
            "executionTimeSeconds": 0,
            "startTime": "",
            "endTime": "",
        }

    def _save(self):
        with open(OUTPUT_RESULTS_JSON, "w") as results_json:
            json.dump(self._results, results_json, indent=2)

        logger.info(f"Results saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_job(self, job: "Job"):
        job_result = {}

        job_result["id"] = job.get_id()
        job_result["status"] = job.get_status()
        job_result["runOk"] = job.get_run_ok()
        job_result["step"] = job.get_step()  # idk about this one
        job_result["startTime"] = (
            job.get_start_time().isoformat() if job.get_start_time() is not None else ""
        )
        job_result["resolutionTime"] = (
            job.get_resolution_time().isoformat()
            if job.get_resolution_time() is not None
            else ""
        )
        job_result["caseDirectory"] = job.get_case_directory()
        job_result["assetsDirectory"] = job.get_assets_directory()
        job_result["point"] = get_serialized_point(job.get_point())
        job_result["objectives"] = get_serialized_objectives(job.get_objectives())

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

        logger.info(f"Job saved successfully in {OUTPUT_RESULTS_JSON}")

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

        logger.info(f"Search saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_solutions(self, solutions: list["Solution"]):
        solutions_result = []

        for solution in solutions:
            parameters = []
            objectives = []

            for parameter in solution.get_parameters():
                parameters.append(
                    {
                        "id": parameter.get_id(),
                        "name": parameter.get_name(),
                        "min": parameter.get_min(),
                        "max": parameter.get_max(),
                        "value": parameter.get_value(),
                    }
                )

            for objective in solution.get_objectives():
                objectives.append(
                    {
                        "id": objective.get_id(),
                        "name": objective.get_name(),
                        "type": objective.get_type(),
                        "value": objective.get_value(),
                    }
                )

            solutions_result.append(
                {"parameters": parameters, "objectives": objectives}
            )

        self._results["solutions"] = solutions_result

        self._save()

        logger.info(f"Solution saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_execution_time(self, execution_time: int):
        self._results["executionTimeSeconds"] = execution_time

        self._save()

        logger.info(f"Execution time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_start_time(self, start_time: datetime):
        self._results["startTime"] = start_time.isoformat()

        self._save()

        logger.info(f"Start time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None

    def save_end_time(self, end_time: datetime):
        self._results["endTime"] = end_time.isoformat()

        self._save()

        logger.info(f"End time saved successfully in {OUTPUT_RESULTS_JSON}")

        return None
