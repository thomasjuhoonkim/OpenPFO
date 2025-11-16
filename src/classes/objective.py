from constants.objective import ObjectiveType


class Objective:
    def __init__(self, name: str, type: ObjectiveType):
        self._name = name
        self._type = type

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type
