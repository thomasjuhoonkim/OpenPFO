from classes.variable import Variable
from classes.point import Point


class TestPoint:
    def _make_single(self):
        return Point(variables=[Variable(name="alpha", id="alpha", value=5.0)])

    def _make_multi(self):
        return Point(variables=[
            Variable(name="alpha", id="alpha", value=5.0),
            Variable(name="beta",  id="beta",  value=3.0),
        ])

    def test_get_representation_single(self):
        assert self._make_single().get_representation() == "(alpha: 5.0)"

    def test_get_representation_multi(self):
        assert self._make_multi().get_representation() == "(alpha: 5.0, beta: 3.0)"

    def test_serialize_contains_representation(self):
        d = self._make_single().serialize()
        assert "representation" in d
        assert d["representation"] == "(alpha: 5.0)"

    def test_serialize_variables_list(self):
        d = self._make_multi().serialize()
        assert len(d["variables"]) == 2

    def test_from_dict_round_trip(self):
        original = self._make_multi()
        restored = Point.from_dict(original.serialize())
        orig_vars = original.get_variables()
        rest_vars = restored.get_variables()
        assert len(rest_vars) == len(orig_vars)
        for o, r in zip(orig_vars, rest_vars):
            assert r.get_name() == o.get_name()
            assert r.get_id() == o.get_id()
            assert r.get_value() == o.get_value()
