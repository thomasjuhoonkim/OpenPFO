from classes.objective import Objective


def get_serialized_objectives(objectives: list[Objective]):
    return [
        {
            "id": objective.get_id(),
            "name": objective.get_name(),
            "type": objective.get_type(),
            "value": objective.get_value(),
        }
        for objective in objectives
    ]
