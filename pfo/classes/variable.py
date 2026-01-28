class Variable:
    def __init__(self, name: str, id: str, value: float):
        self._name = name
        self._id = id
        self._value = value

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_value(self):
        return self._value

    def serialize(self):
        return {
            "id": self._id,
            "name": self._name,
            "value": self._value,
        }

    @classmethod
    def from_dict(cls, variable: dict):
        return cls(name=variable["name"], id=variable["id"], value=variable["value"])
