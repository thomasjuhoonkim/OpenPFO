from constants.objective import ObjectiveType


class Objective:
    def __init__(self, id: str, name: str, type: ObjectiveType):
        self._id = id
        self._name = name
        self._type = type
        self._value = None

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def set_value(self, value: float):
        self._value = value

    def get_value(self):
        return self._value

    def get_pymoo_value(self):
        return -1 * self._value if self._type == "maximize" else self._value

    def serialize(self):
        return {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "value": self._value,
        }

    @classmethod
    def from_dict(cls, objective: dict):
        objective_object = cls(
            id=objective["id"], name=objective["name"], type=objective["type"]
        )
        if objective["value"] is not None:
            objective_object.set_value(value=objective["value"])
        return objective_object
