# system
import os

# classes
from classes.functions import ExecuteSolverParameters, ExecuteSolverReturn

# simple-slurm
from simple_slurm import Slurm


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
):
    """
    The execute_solver function is used to create the geometry for each grid
    point in the design space.
    """
    assets_directory = execute_solver_parameters.output_assets_directory
    processors_per_job = execute_solver_parameters.processors_per_job
    logger = execute_solver_parameters.logger
    job_id = execute_solver_parameters.job_id
    point = execute_solver_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    EXECUTE_SOLVER_RETURN = ExecuteSolverReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_SOLVER_RETURN
