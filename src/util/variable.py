class Variable:
    def __init__(self, name, cell, value):
        self._name = name
        self._cell = cell
        self._value = value

    def get_name(self):
        return self._name

    def get_cell(self):
        return self._cell

    def get_value(self):
        return self._value
