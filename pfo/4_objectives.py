# classes
from classes.functions import ObjectivesParameters, ObjectivesReturn
from classes.objective import Objective


def objectives(
    objectives_parameters: ObjectivesParameters,
) -> ObjectivesReturn:
    """
    This function is used to extract objectives and export data for each job.

    NOTE: This function MUST modify the original list of objectives and return it.
    """

    def get_objective_by_id(objectives: list[Objective], id: str):
        return next((o for o in objectives if o.get_id() == id), None)

    assets_directory = objectives_parameters.output_assets_directory
    processors_per_job = objectives_parameters.processors_per_job
    objectives = objectives_parameters.objectives
    logger = objectives_parameters.logger
    point = objectives_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    OBJECTIVES_RETURN = ObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return OBJECTIVES_RETURN
