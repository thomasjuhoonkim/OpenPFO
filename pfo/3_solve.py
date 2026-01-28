# classes
from classes.functions import SolveParameters, SolveReturn


def solve(
    solve_parameters: SolveParameters,
):
    """
    This function is used to solve the mesh for each point in the design space.
    """

    assets_directory = solve_parameters.output_assets_directory
    processors_per_job = solve_parameters.processors_per_job
    job_id = solve_parameters.job_id
    logger = solve_parameters.logger
    point = solve_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    SOLVE_RETURN = SolveReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return SOLVE_RETURN
