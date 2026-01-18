class Parameter:
    def __init__(self, name: str, id: str, min: float, max: float):
        self._name = name
        self._id = id
        self._min = min
        self._max = max

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_min(self):
        return self._min

    def get_max(self):
        return self._max

    def set_value(self, value: float):
        self._value = value

    def get_value(self):
        return self._value
