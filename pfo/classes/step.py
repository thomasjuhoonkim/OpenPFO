# datetime
from datetime import datetime

# constants
from constants.step import StepId


class Step:
    def __init__(
        self, id: StepId, run_ok: bool, start_time: datetime, end_time: datetime
    ):
        self._id = id
        self._run_ok = run_ok
        self._start_time = start_time
        self._end_time = end_time

    def get_id(self):
        return self._id

    def get_run_ok(self):
        return self._run_ok

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_execution_time(self):
        time_diff = self._end_time - self._start_time
        return time_diff.total_seconds()
