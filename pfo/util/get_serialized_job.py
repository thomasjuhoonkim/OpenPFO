# typing
from typing import TYPE_CHECKING

# classes
if TYPE_CHECKING:
    from classes.job import Job

# util
from util.get_serialized_objective import get_serialized_objective
from util.get_serialized_point import get_serialized_point
from util.get_serialized_steps import get_serialized_steps


def get_serialized_job(job: "Job"):
    return {
        "id": job.get_id(),
        "status": job.get_status(),
        "runOk": job.get_run_ok(),
        "steps": get_serialized_steps(steps=job.get_steps()),
        "startTime": job.get_start_time().isoformat(),
        "endTime": job.get_end_time().isoformat(),
        "executionTime": (job.get_end_time() - job.get_start_time()).total_seconds(),
        "caseDirectory": job.get_case_directory(),
        "assetsDirectory": job.get_assets_directory(),
        "point": get_serialized_point(point=job.get_point()),
        "objectives": [
            get_serialized_objective(objective=objective)
            for objective in job.get_objectives()
        ],
    }
