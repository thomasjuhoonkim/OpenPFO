class Parameter:
    def __init__(self, name: str, id: str, min: float, max: float):
        self._name = name
        self._id = id
        self._min = min
        self._max = max
        self._value = None

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

    def serialize(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "min": self.get_min(),
            "max": self.get_max(),
            "value": self.get_value(),
        }

    @classmethod
    def from_dict(cls, parameter: dict):
        parameter_object = Parameter(
            name=parameter["name"],
            id=parameter["id"],
            min=parameter["min"],
            max=parameter["max"],
            value=parameter["value"],
        )
        if parameter["value"] is not None:
            parameter_object.set_value(value=parameter["value"])
        return parameter_object
