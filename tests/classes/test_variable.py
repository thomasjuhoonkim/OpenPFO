from classes.variable import Variable


class TestVariable:
    def _make(self):
        return Variable(name="alpha", id="alpha", value=3.5)

    def test_getters(self):
        v = self._make()
        assert v.get_name() == "alpha"
        assert v.get_id() == "alpha"
        assert v.get_value() == 3.5

    def test_serialize_keys(self):
        d = self._make().serialize()
        assert set(d.keys()) == {"id", "name", "value"}

    def test_serialize_values(self):
        d = self._make().serialize()
        assert d["id"] == "alpha"
        assert d["name"] == "alpha"
        assert d["value"] == 3.5

    def test_from_dict_round_trip(self):
        original = Variable(name="speed", id="spd", value=7.2)
        restored = Variable.from_dict(original.serialize())
        assert restored.get_name() == original.get_name()
        assert restored.get_id() == original.get_id()
        assert restored.get_value() == original.get_value()
