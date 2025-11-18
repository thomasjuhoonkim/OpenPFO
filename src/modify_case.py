# system
import shutil

# classes
from classes.functions import ModifyCaseParameters


def modify_case(modify_case_parameters: ModifyCaseParameters) -> None:
    """
    This function is used to modify each OpenFOAM case for each run. This is a
    critical step if you need to set value(s) to OpenFOAM functions for each
    design parameter.

    You have access to the case path and the geometry modeling client.

    This function does NOT return anything.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    output_case_directory = modify_case_parameters.output_case_directory
    output_geometry_filepath = modify_case_parameters.output_geometry_filepath
    logger = modify_case_parameters.logger

    # copy geometry into case trisurface directory
    trisurface_geometry_filepath = (
        f"{output_case_directory}/constant/triSurface/jobGeometry.stl"
    )
    shutil.copy(
        src=output_geometry_filepath,
        dst=trisurface_geometry_filepath,
    )
    logger.info(
        f"Copied geometry {output_geometry_filepath} into {trisurface_geometry_filepath}"
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
