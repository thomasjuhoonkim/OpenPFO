from constants.modeler import AbstractModeler
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory


def modify_case(case_directory: str, modeler: AbstractModeler):
    """
    This function is used to modify each OpenFOAM case for each run. This is a
    critical step if you need to set value(s) to OpenFOAM functions for each
    design parameter.

    You have access to the case path and the geometry modeling client.

    This function does NOT return anything.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    # SolutionDirectory(case_directory)

    # print(case, modeler)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
