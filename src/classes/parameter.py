class Parameter:
    def __init__(self, name: str, cell: str, min: float, max: float):
        self._name = name
        self._cell = cell
        self._min = min
        self._max = max

    def get_name(self):
        return self._name

    def get_cell(self):
        return self._cell

    def get_min(self):
        return self._min

    def get_max(self):
        return self._max
