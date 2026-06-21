from classes.variable import Variable
from classes.point import Point
from classes.objective import Objective
from classes.solution import Solution
from constants.objective import ObjectiveType
from util.format_solutions import format_solutions


def _make_solution(alpha_val=5.0, drag_val=0.03):
    point = Point(variables=[Variable(name="alpha", id="alpha", value=alpha_val)])
    drag = Objective(id="drag", name="Drag", type=ObjectiveType.MINIMIZE)
    drag.set_value(drag_val)
    return Solution(point=point, objectives=[drag])


class TestFormatSolutions:
    def test_starts_with_newline(self):
        assert format_solutions([_make_solution()]).startswith("\n")

    def test_single_solution_label(self):
        assert "SOLUTION 0" in format_solutions([_make_solution()])

    def test_multiple_solution_labels(self):
        result = format_solutions([_make_solution(5.0), _make_solution(7.0)])
        assert "SOLUTION 0" in result
        assert "SOLUTION 1" in result

    def test_solutions_separated_by_blank_line(self):
        result = format_solutions([_make_solution(5.0), _make_solution(7.0)])
        assert "\n\n" in result

    def test_contains_variable_and_objective_data(self):
        result = format_solutions([_make_solution(alpha_val=3.14, drag_val=0.05)])
        assert "alpha" in result
        assert "Drag" in result

    def test_empty_list_returns_newline(self):
        assert format_solutions([]) == "\n"
