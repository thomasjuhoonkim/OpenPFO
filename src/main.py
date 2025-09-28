# system
import tomllib

from util.workflow import Workflow
from util.search import Search
from util.parameter import Parameter

# ==============================================================================

# config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

if __name__ == "__main__":
    workflow = Workflow()

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

    # instantiate initial search
    search_id = workflow.generate_search_id()
    search = Search(search_id=search_id, parameters=parameters)
    search.create_all_jobs()

    print(search.get_jobs())
    jobs = search.get_jobs()
    for job in jobs:
        job.visualize_geometry()
