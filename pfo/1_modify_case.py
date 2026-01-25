# system
import subprocess

# classes
from classes.functions import ModifyCaseParameters, ModifyCaseReturn

# PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def modify_case(modify_case_parameters: ModifyCaseParameters):
    """
    This function is used to modify each OpenFOAM case for each run. This is a
    critical step if you need to set value(s) to OpenFOAM functions for each
    design parameter.

    You have access to the case path and the geometry modeling client.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    geometry_filepath = modify_case_parameters.output_geometry_filepath
    case_directory = modify_case_parameters.output_case_directory
    logger = modify_case_parameters.logger

    commands = [
        f"cp {geometry_filepath} {case_directory}/original.stl",
    ]

    for command in commands:
        subprocess.run(command.split(" "), capture_output=True, text=True, check=True)
        logger.info(f"Successfully ran {command}")

    MODIFY_CASE_RETURN = ModifyCaseReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MODIFY_CASE_RETURN
