# classes
from classes.functions import PrepareParameters, PrepareReturn

# PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory


def prepare(prepare_parameters: PrepareParameters):
    """
    This function is used to prepare each job.
    """

    job_directory = prepare_parameters.job_directory
    processors_per_job = prepare_parameters.processors_per_job
    job_id = prepare_parameters.job_id
    logger = prepare_parameters.logger
    point = prepare_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_template = SolutionDirectory("input/case_template")
    case_template.cloneCase(job_directory)

    # ==========================================================================

    # case
    decompose_par_dict_filepath = f"{job_directory}/system/decomposeParDict"
    decompose_par_dict = ParsedParameterFile(decompose_par_dict_filepath)

    decompose_par_dict["numberOfSubdomains"] = processors_per_job

    decompose_par_dict.writeFile()

    # ==========================================================================

    # postProcessing file modifications
    root_chord_variable = point.get_variables()[0]
    root_chord = root_chord_variable.get_value()
    tip_chord = 0.10  # metres
    taper_ratio = tip_chord / root_chord
    l_ref = (
        root_chord * (2 / 3) * ((1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio))
    )
    a_ref = l_ref * 0.9
    c_of_r = root_chord - l_ref + (0.25 * l_ref)

    # case
    control_dict_filepath = f"{job_directory}/system/controlDict"
    control_dict_file = ParsedParameterFile(control_dict_filepath)

    # modify values
    control_dict_file["functions"]["forceCoeffs1"]["lRef"] = l_ref
    control_dict_file["functions"]["forceCoeffs1"]["Aref"] = a_ref
    control_dict_file["functions"]["forceCoeffs1"]["CofR"] = f"({c_of_r} 0 0)"

    # write
    control_dict_file.writeFile()

    PREPARE_RETURN = PrepareReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return PREPARE_RETURN
