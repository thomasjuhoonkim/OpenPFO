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

    # meta
    meta.add_meta("case", job_id)

    PREPARE_RETURN = PrepareReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return PREPARE_RETURN
