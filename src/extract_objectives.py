import fluidfoam

# classes
from classes.functions import ExtractObjectivesParameters, ExtractObjectivesReturn


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

    force = fluidfoam.readforce(
        path=extract_objectives_parameters.output_case_directory,
        namepatch="forceCoeffs1",
        time_name="0",
        name="coefficient",
    )
    Cd = force[-1][1]  # latest time & second index (Cd)
    objectives = [Cd]
    EXTRACT_OBJECTIVES_RETURN = ExtractObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_OBJECTIVES_RETURN
