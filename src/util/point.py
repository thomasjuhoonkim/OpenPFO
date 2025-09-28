from util.variable import Variable


class Point:
    def __init__(self, variables: list[Variable]):
        self._variables = variables

    def get_variables(self):
        return self._variables

    def get_point_representation(self):
        values = []
        for variable in self._variables:
            values.append(str(variable.get_value()))

        return f"({', '.join(values)})"
