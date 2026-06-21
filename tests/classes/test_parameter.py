from classes.parameter import Parameter


class TestParameter:
    def _make(self):
        return Parameter(name="sweep", id="sweep", min=5.0, max=85.0)

    def test_getters(self):
        p = self._make()
        assert p.get_name() == "sweep"
        assert p.get_id() == "sweep"
        assert p.get_min() == 5.0
        assert p.get_max() == 85.0

    def test_initially_no_value(self):
        assert self._make().get_value() is None

    def test_set_value(self):
        p = self._make()
        p.set_value(45.0)
        assert p.get_value() == 45.0

    def test_serialize_keys(self):
        assert set(self._make().serialize().keys()) == {"id", "name", "min", "max", "value"}

    def test_serialize_values(self):
        d = self._make().serialize()
        assert d["min"] == 5.0
        assert d["max"] == 85.0
        assert d["value"] is None

    def test_from_dict_with_value(self):
        p = Parameter.from_dict({"name": "sweep", "id": "sweep", "min": 5.0, "max": 85.0, "value": 45.0})
        assert p.get_name() == "sweep"
        assert p.get_id() == "sweep"
        assert p.get_min() == 5.0
        assert p.get_max() == 85.0
        assert p.get_value() == 45.0

    def test_from_dict_with_none_value(self):
        p = Parameter.from_dict({"name": "sweep", "id": "sweep", "min": 5.0, "max": 85.0, "value": None})
        assert p.get_value() is None
