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
    point = modify_case_parameters.point

    commands = [
        f"cp {geometry_filepath} {case_directory}/original.stl",
    ]

    for command in commands:
        subprocess.run(command.split(" "), capture_output=True, text=True, check=True)
        logger.info(f"Successfully ran {command}")

    # postProcessing file modifications
    root_chord_variable = point.get_variables()[0]
    root_chord = root_chord_variable.get_value()
    tip_chord = 0.10  # metres
    taper_ratio = tip_chord / root_chord
    l_ref = (
        root_chord * (2 / 3) * ((1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio))
    )
    a_ref = l_ref / 0.9
    c_of_r = root_chord - l_ref + (0.25 * l_ref)

    # case
    control_dict_filepath = f"{case_directory}/system/controlDict"
    control_dict_file = ParsedParameterFile(control_dict_filepath)

    # modify values
    control_dict_file["functions"]["forceCoeffs1"]["lRef"] = l_ref
    control_dict_file["functions"]["forceCoeffs1"]["Aref"] = a_ref
    control_dict_file["functions"]["forceCoeffs1"]["CofR"] = f"({c_of_r} 0 0)"

    # write
    control_dict_file.writeFile()

    MODIFY_CASE_RETURN = ModifyCaseReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MODIFY_CASE_RETURN
