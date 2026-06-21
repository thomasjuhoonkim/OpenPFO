import pytest
from classes.objective import Objective
from constants.objective import ObjectiveType


class TestObjective:
    def _make_minimize(self):
        return Objective(id="drag", name="Drag", type=ObjectiveType.MINIMIZE)

    def _make_maximize(self):
        return Objective(id="lift", name="Lift", type=ObjectiveType.MAXIMIZE)

    def test_initially_invalid(self):
        obj = self._make_minimize()
        assert obj.is_valid() is False
        assert obj.get_value() is None

    def test_set_value_makes_valid(self):
        obj = self._make_minimize()
        obj.set_value(42.0)
        assert obj.is_valid() is True
        assert obj.get_value() == 42.0

    def test_type_minimize(self):
        assert self._make_minimize().get_type() == ObjectiveType.MINIMIZE

    def test_type_maximize(self):
        assert self._make_maximize().get_type() == ObjectiveType.MAXIMIZE

    def test_serialize_without_value(self):
        d = self._make_minimize().serialize()
        assert d == {"id": "drag", "name": "Drag", "type": "minimize", "value": None}

    def test_serialize_with_value(self):
        obj = self._make_maximize()
        obj.set_value(1.23)
        d = obj.serialize()
        assert d["value"] == 1.23
        assert d["type"] == "maximize"

    def test_from_dict_round_trip_none_value(self):
        original = self._make_minimize()
        restored = Objective.from_dict(original.serialize())
        assert restored.get_id() == original.get_id()
        assert restored.get_name() == original.get_name()
        assert restored.get_type() == original.get_type()
        assert restored.is_valid() is False

    def test_from_dict_round_trip_with_value(self):
        original = self._make_maximize()
        original.set_value(99.9)
        restored = Objective.from_dict(original.serialize())
        assert restored.get_value() == pytest.approx(99.9)
        assert restored.is_valid() is True
