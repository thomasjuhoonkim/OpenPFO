from classes.objective import Objective


def get_objective_by_id(objectives: list[Objective], id: str):
    return next((o for o in objectives if o.get_id() == id), None)
