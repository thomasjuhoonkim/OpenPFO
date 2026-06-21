import pytest
from unittest.mock import patch
from util.get_linear_points import get_linear_points
from .conftest import mock_parameters


class TestGetLinearPoints:
    def test_returns_correct_count(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(5)
        assert len(points) == 5

    def test_first_point_at_lower_bounds(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(5)
        vars_ = {v.get_id(): v.get_value() for v in points[0].get_variables()}
        assert vars_["alpha"] == pytest.approx(0.0)
        assert vars_["beta"] == pytest.approx(1.0)

    def test_last_point_at_upper_bounds(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(5)
        vars_ = {v.get_id(): v.get_value() for v in points[-1].get_variables()}
        assert vars_["alpha"] == pytest.approx(10.0)
        assert vars_["beta"] == pytest.approx(5.0)

    def test_points_are_evenly_spaced(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(6)
        alpha_values = [
            next(v.get_value() for v in p.get_variables() if v.get_id() == "alpha")
            for p in points
        ]
        diffs = [alpha_values[i + 1] - alpha_values[i] for i in range(len(alpha_values) - 1)]
        for d in diffs:
            assert d == pytest.approx(2.0)

    def test_variable_names_and_ids_are_set(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(3)
        for point in points:
            assert {v.get_id() for v in point.get_variables()} == {"alpha", "beta"}
            assert {v.get_name() for v in point.get_variables()} == {"alpha", "beta"}

    def test_two_points_gives_bounds(self):
        with patch("util.get_linear_points.get_config_parameters", return_value=mock_parameters()):
            points = get_linear_points(2)
        alpha_values = [
            next(v.get_value() for v in p.get_variables() if v.get_id() == "alpha")
            for p in points
        ]
        assert alpha_values[0] == pytest.approx(0.0)
        assert alpha_values[1] == pytest.approx(10.0)
