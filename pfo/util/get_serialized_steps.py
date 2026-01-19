# classes
from classes.step import Step


def get_serialized_steps(steps: list[Step]):
    return [
        {
            "id": step.get_id().value,
            "runOk": step.get_run_ok(),
            "startTime": step.get_start_time().isoformat(),
            "endTime": step.get_end_time().isoformat(),
            "executionTime": step.get_execution_time(),
        }
        for step in steps
    ]
