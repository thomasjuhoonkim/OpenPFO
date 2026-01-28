# classes
from classes.functions import ExtractAssetsParameters, ExtractAssetsReturn

# simple-slurm
from simple_slurm import Slurm


def extract_assets(
    extract_assets_parameters: ExtractAssetsParameters,
):
    """
    The extract_assets function is used to add side effects to your optimization
    workflow such as image extractation and data analysis. The extract_assets
    function runs AFTER execute_solver and extract_objectives.

    All data from this function will be available to export after the full
    workflow has completed. You may store any data from this function in the
    provided assets output directory.
    """

    output_directory = extract_assets_parameters.output_assets_directory
    processors_per_job = extract_assets_parameters.processors_per_job
    logger = extract_assets_parameters.logger
    job_id = extract_assets_parameters.job_id
    point = extract_assets_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    EXTRACT_ASSETS_RETURN = ExtractAssetsReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_ASSETS_RETURN
