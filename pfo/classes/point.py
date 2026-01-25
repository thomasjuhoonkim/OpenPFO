# classes
from classes.variable import Variable


class Point:
    def __init__(self, variables: list[Variable], job_id=""):
        self._job_id = job_id
        self._variables = variables

    def set_job_id(self, job_id: str):
        self._job_id = job_id

    def get_variables(self):
        return self._variables

    def get_representation(self):
        values = []
        for variable in self._variables:
            values.append(f"{variable.get_name()}: {variable.get_value()}")

        return f"({', '.join(values)})"

    def serialize(self):
        return {
            "jobId": self._job_id,
            "representation": self.get_representation(),
            "variables": [variable.serialize() for variable in self._variables],
        }

    @classmethod
    def from_dict(cls, point: dict):
        return Point(
            job_id=point["jobId"],
            variables=[Variable.from_dict(variable) for variable in point["variables"]],
        )
