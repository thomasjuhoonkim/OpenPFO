# system
import os

# classes
from classes.functions import CreateMeshParameters, CreateMeshReturn

# simple-slurm
from simple_slurm import Slurm


def create_mesh(
    create_mesh_parameters: CreateMeshParameters,
):
    """
    The create_mesh function is used to create the geometry for each grid
    point in the design space.
    """
    assets_directory = create_mesh_parameters.output_assets_directory
    processors_per_job = create_mesh_parameters.processors_per_job
    logger = create_mesh_parameters.logger
    job_id = create_mesh_parameters.job_id
    point = create_mesh_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    CREATE_MESH_RETURN = CreateMeshReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_MESH_RETURN
