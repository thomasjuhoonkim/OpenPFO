from unittest.mock import patch
from util.get_random_points import get_random_points
from .conftest import mock_parameters


class TestGetRandomPoints:
    def test_returns_correct_count(self):
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(10)
        assert len(points) == 10

    def test_alpha_values_within_bounds(self):
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(50)
        for point in points:
            for v in point.get_variables():
                if v.get_id() == "alpha":
                    assert 0.0 <= v.get_value() <= 10.0

    def test_beta_values_within_bounds(self):
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(50)
        for point in points:
            for v in point.get_variables():
                if v.get_id() == "beta":
                    assert 1.0 <= v.get_value() <= 5.0

    def test_variable_names_and_ids_are_set(self):
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(5)
        for point in points:
            assert {v.get_id() for v in point.get_variables()} == {"alpha", "beta"}

    def test_each_point_has_correct_variable_count(self):
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(5)
        for point in points:
            assert len(point.get_variables()) == 2

    def test_produces_distinct_points(self):
        """Random sampling from a continuous space should not produce all-identical points."""
        with patch("util.get_random_points.get_config_parameters", return_value=mock_parameters()):
            points = get_random_points(20)
        alpha_values = [
            next(v.get_value() for v in p.get_variables() if v.get_id() == "alpha")
            for p in points
        ]
        assert len(set(alpha_values)) > 1
