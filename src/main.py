# system
import tomllib

from classes.workflow import Workflow
from classes.parameter import Parameter
from optimizers import NoOptimizer

# ==============================================================================

# config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

if __name__ == "__main__":
    # configure initial parameters
    PARAMS = config["model"]["parameters"]
    parameters = []
    for param in PARAMS:
        parameter = Parameter(
            name=param["name"],
            cell=param["cell"],
            min=param["min"],
            max=param["max"],
            grid_points=param["grid_points"],
        )
        parameters.append(parameter)

    # initialize optimizer
    optimizer = NoOptimizer()

    # initialize workflow
    workflow = Workflow(parameters=parameters, optimizer=optimizer)
