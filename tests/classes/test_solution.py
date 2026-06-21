from classes.variable import Variable
from classes.point import Point
from classes.objective import Objective
from classes.solution import Solution
from constants.objective import ObjectiveType


class TestSolution:
    def _make(self):
        point = Point(variables=[
            Variable(name="alpha", id="alpha", value=5.0),
            Variable(name="beta",  id="beta",  value=2.5),
        ])
        drag = Objective(id="drag", name="Drag", type=ObjectiveType.MINIMIZE)
        drag.set_value(0.03)
        lift = Objective(id="lift", name="Lift", type=ObjectiveType.MAXIMIZE)
        lift.set_value(1.2)
        return Solution(point=point, objectives=[drag, lift])

    def test_get_point(self):
        assert len(self._make().get_point().get_variables()) == 2

    def test_get_objectives(self):
        assert len(self._make().get_objectives()) == 2

    def test_representation_contains_section_headers(self):
        rep = self._make().get_solution_representation()
        assert "VARIABLES" in rep
        assert "OBJECTIVES" in rep

    def test_representation_contains_variable_names(self):
        rep = self._make().get_solution_representation()
        assert "alpha" in rep
        assert "beta" in rep

    def test_representation_contains_objective_values(self):
        rep = self._make().get_solution_representation()
        assert "Drag" in rep
        assert "Lift" in rep
        assert "0.03" in rep
        assert "1.2" in rep
