# classes
from classes.objective import Objective

# util
from util.get_config import get_config

config = get_config()

CONFIG_OBJECTIVES = config["optimizer"]["objectives"]


def get_config_objectives() -> list[Objective]:
    objectives = []

    for config_objective in CONFIG_OBJECTIVES:
        objective = Objective(
            id=config_objective["id"],
            name=config_objective["name"],
            type=config_objective["type"],
        )
        objectives.append(objective)

    return objectives
