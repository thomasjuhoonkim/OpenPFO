# system
import math
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

    case_directory = modify_case_parameters.output_case_directory
    logger = modify_case_parameters.logger
    point = modify_case_parameters.point

    commands = [
        f"cp input/airfoil0.stl {case_directory}/original.stl",
    ]

    for command in commands:
        subprocess.run(command.split(" "), capture_output=True, text=True, check=True)
        logger.info(f"Successfully ran {command}")

    # postProcessing file modifications
    aoa_variable = point.get_variables()[0]
    aoa = aoa_variable.get_value()

    multiplier = (660 - (13.97 * math.sin(aoa))) / 1000
    a = multiplier * math.cos(aoa)
    b = 0
    c = multiplier * math.sin(aoa)

    # case
    control_dict_filepath = f"{case_directory}/system/controlDict"
    control_dict_file = ParsedParameterFile(control_dict_filepath)

    # modify values
    control_dict_file["functions"]["forceCoeffs1"]["CofR"] = f"({a} {b} {c})"

    # write
    control_dict_file.writeFile()

    MODIFY_CASE_RETURN = ModifyCaseReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MODIFY_CASE_RETURN
