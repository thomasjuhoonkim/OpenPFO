# classes
from constants.objective import ObjectiveType
import numpy as np


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

    def _get_default_value(self):
        FLOAT_MAX = np.finfo(np.float64).max
        value = self._value
        if self._value is None:
            value = FLOAT_MAX
        return value

    def get_minimized_value(self):
        """When the objective function is looking to minimize all values, you need to invert values you are trying to maximize"""
        value = self._get_default_value()
        if self._type == "maximize":
            return -1 * value
        else:
            return value

    def get_maximized_value(self):
        """When the objectuve function is looking to maximize all values, you need to invert vlaues you are trying to minimize"""
        value = self._get_default_value()
        if self._type == "minimize":
            return -1 * value
        else:
            return value

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
