# classes
from classes.objective import Objective

# util
from util.get_config import get_config

config = get_config()

CONFIG_OBJECTIVES = config["optimizer"]["objective"]


def get_objectives() -> list[Objective]:
    objectives = []

    for config_objective in CONFIG_OBJECTIVES:
        objective = Objective(
            name=config_objective["name"],
            type=config_objective["type"],
        )
        objectives.append(objective)

    return objectives
