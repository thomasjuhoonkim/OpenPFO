# fluidfoam
import fluidfoam

# classes
from classes.functions import ExtractObjectivesParameters, ExtractObjectivesReturn
from classes.objective import Objective


def extract_objectives(
    extract_objectives_parameters: ExtractObjectivesParameters,
) -> ExtractObjectivesReturn:
    """
    The extract_objectives function is used to rank simulation results in a
    multi-objective optimization case.

    The extract_objectives MUST process OpenFOAM results for each grid point in
    the design space using a post-processor of your choice.

    Optionally, you can add side effects to your optimization such as image
    extractation and data analysis using inputs/extract_assets.py

    NOTE: This function MUST return a list of objectives to MINIMIZE for.
    """

    def get_objective_by_id(objectives: list[Objective], id: str):
        return next((o for o in objectives if o.get_id() == id), None)

    """ ======================= YOUR CODE BELOW HERE ======================= """

    assets_directory = extract_objectives_parameters.output_assets_directory
    objectives = extract_objectives_parameters.objectives
    logger = extract_objectives_parameters.logger

    EXTRACT_OBJECTIVES_RETURN = ExtractObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_OBJECTIVES_RETURN
