# classes
from classes.parameter import Parameter
from util.get_config import get_config

config = get_config()

CONFIG_PARAMETERS = config["model"]["parameter"]


def get_initial_parameters() -> list[Parameter]:
    parameters = []
    for config_parameter in CONFIG_PARAMETERS:
        parameter = Parameter(
            name=config_parameter["name"],
            id=config_parameter["id"],
            min=config_parameter["min"],
            max=config_parameter["max"],
        )
        parameters.append(parameter)

    return parameters
