# classes
from classes.functions import ExecuteCleanupParameters, ExecuteCleanupReturn

# simple-slurm
from simple_slurm import Slurm


def execute_cleanup(
    execute_cleanup_parameters: ExecuteCleanupParameters,
):
    """
    The execute_cleanup function used to clean up solver artifacts after each job.
    """
    assets_directory = execute_cleanup_parameters.output_assets_directory
    processors_per_job = execute_cleanup_parameters.processors_per_job
    logger = execute_cleanup_parameters.logger
    job_id = execute_cleanup_parameters.job_id
    point = execute_cleanup_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    EXECUTE_CLEANUP_RETURN = ExecuteCleanupReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_CLEANUP_RETURN
