# classes
from classes.functions import CleanupParameters, CleanupReturn


def cleanup(
    cleanup_parameters: CleanupParameters,
):
    """
    This function is used to clean up artifacts after each job.
    """

    job_directory = cleanup_parameters.job_directory
    processors_per_job = cleanup_parameters.processors_per_job
    logger = cleanup_parameters.logger
    job_id = cleanup_parameters.job_id
    point = cleanup_parameters.point
    meta = cleanup_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    CLEANUP_RETURN = CleanupReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CLEANUP_RETURN
