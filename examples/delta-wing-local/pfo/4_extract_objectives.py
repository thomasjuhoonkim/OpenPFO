# fluidfoam
import fluidfoam

# classes
from classes.functions import ExtractObjectivesParameters, ExtractObjectivesReturn

# util
from util.get_objective_by_id import get_objective_by_id


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

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = extract_objectives_parameters.output_case_directory
    objectives = extract_objectives_parameters.objectives
    logger = extract_objectives_parameters.logger

    force = fluidfoam.readforce(
        path=case_directory,
        namepatch="forceCoeffs1",
        time_name="0",
        name="coefficient",
    )

    c_d = get_objective_by_id(objectives=objectives, id="cd")
    c_d.set_value(force[-1][1])  # latest time & second index (Cd - maximize)

    c_l = get_objective_by_id(objectives=objectives, id="cl")
    c_l.set_value(force[-1][4])  # latest time & fourth index (Cl - minimize)

    logger.info("Successfully extracted objectives")

    EXTRACT_OBJECTIVES_RETURN = ExtractObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_OBJECTIVES_RETURN
