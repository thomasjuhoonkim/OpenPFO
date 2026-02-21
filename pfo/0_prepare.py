# math
import math

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
    meta = prepare_parameters.meta

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
    sweep_variable = point.get_variables()[2]
    sweep = sweep_variable.get_value()
    root_chord = 0.000298 * (sweep**2) + 0.0308 * (sweep) + 0.143
    tip_chord = 0.135  # metres
    taper_ratio = tip_chord / root_chord
    l_ref = (
        root_chord * (2 / 3) * ((1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio))
    )
    a_ref = l_ref * 0.9
    c_of_r = (l_ref / 4) + ((4 * (1 + taper_ratio) / (6 * 1 + taper_ratio))) * math.tan(
        sweep * math.pi / 180
    )

    # case
    control_dict_filepath = f"{job_directory}/system/controlDict"
    control_dict_file = ParsedParameterFile(control_dict_filepath)

    # modify values
    control_dict_file["functions"]["forceCoeffs1"]["lRef"] = l_ref
    control_dict_file["functions"]["forceCoeffs1"]["Aref"] = a_ref
    CofR = f"({c_of_r} 0 0)"
    control_dict_file["functions"]["forceCoeffs1"]["CofR"] = CofR
    control_dict_file["functions"]["forces"]["CofR"] = CofR
    control_dict_file["functions"]["binField1"]["CofR"] = CofR

    # write
    control_dict_file.writeFile()

    # meta
    meta.add_meta("case", job_id)
    meta.add_meta("root-chord", root_chord)

    PREPARE_RETURN = PrepareReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return PREPARE_RETURN
