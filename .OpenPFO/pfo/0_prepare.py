# classes
from classes.functions import PrepareParameters, PrepareReturn


def prepare(prepare_parameters: PrepareParameters):
    """
    This function is used to prepare each job.
    """

    assets_directory = prepare_parameters.output_assets_directory
    processors_per_job = prepare_parameters.processors_per_job
    job_id = prepare_parameters.job_id
    logger = prepare_parameters.logger
    point = prepare_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    PREPARE_RETURN = PrepareReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return PREPARE_RETURN
