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

    case_directory = extract_objectives_parameters.output_case_directory
    logger = extract_objectives_parameters.logger

    objectives = []
    run_ok = True
    try:
        force = fluidfoam.readforce(
            path=case_directory,
            namepatch="forceCoeffs1",
            time_name="0",
            name="coefficient",
        )
        c_d = force[-1][1]  # latest time & second index (Cd)
        c_l = force[-1][4]  # latest time & fourth index (Cl)
        objectives = [c_d, c_l]

    except Exception:
        run_ok = False
        logger.exception("fluidfoam readforce failed")

    EXTRACT_OBJECTIVES_RETURN = ExtractObjectivesReturn(
        objectives=objectives, run_ok=run_ok
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_OBJECTIVES_RETURN
