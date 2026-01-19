# classes
from classes.objective import Objective


def get_serialized_objective(objective: Objective):
    return {
        "id": objective.get_id(),
        "name": objective.get_name(),
        "type": objective.get_type(),
        "value": objective.get_value(),
    }
