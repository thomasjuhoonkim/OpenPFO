class Parameter:
    def __init__(self, name: str, cell: str, min: float, max: float, grid_points: int):
        self._name = name
        self._cell = cell
        self._min = min
        self._max = max
        self._grid_points = grid_points

    def get_name(self):
        return self._name

    def get_cell(self):
        return self._cell

    def get_min(self):
        return self._min

    def get_max(self):
        return self._max

    def get_grid_points(self):
        return self._grid_points
