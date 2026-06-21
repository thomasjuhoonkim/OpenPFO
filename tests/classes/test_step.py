import pytest
from datetime import datetime, timedelta, timezone
from classes.step import Step
from constants.step import StepId


class TestStep:
    def _make(self, run_ok=True, duration_seconds=30):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        end   = start + timedelta(seconds=duration_seconds)
        return Step(id=StepId.GEOMETRY, run_ok=run_ok, start_time=start, end_time=end)

    def test_get_execution_time(self):
        assert self._make(duration_seconds=30).get_execution_time() == pytest.approx(30.0)

    def test_get_execution_time_zero(self):
        assert self._make(duration_seconds=0).get_execution_time() == pytest.approx(0.0)

    def test_get_run_ok_true(self):
        assert self._make(run_ok=True).get_run_ok() is True

    def test_get_run_ok_false(self):
        assert self._make(run_ok=False).get_run_ok() is False

    def test_serialize_keys(self):
        d = self._make().serialize()
        assert set(d.keys()) == {"id", "runOk", "startTime", "endTime", "executionTimeSeconds"}

    def test_serialize_id_value(self):
        assert self._make().serialize()["id"] == "geometry"

    def test_serialize_execution_time(self):
        assert self._make(duration_seconds=45).serialize()["executionTimeSeconds"] == pytest.approx(45.0)

    def test_from_dict_round_trip(self):
        original = self._make(run_ok=False, duration_seconds=120)
        restored = Step.from_dict(original.serialize())
        assert restored.get_id() == original.get_id()
        assert restored.get_run_ok() == original.get_run_ok()
        assert restored.get_execution_time() == pytest.approx(original.get_execution_time())
