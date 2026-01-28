# classes
from classes.functions import MeshParameters, MeshReturn


def mesh(
    mesh_parameters: MeshParameters,
):
    """
    The function is used to generate a mesh for each point in the design space.
    """

    job_directory = mesh_parameters.job_directory
    processors_per_job = mesh_parameters.processors_per_job
    logger = mesh_parameters.logger
    job_id = mesh_parameters.job_id
    point = mesh_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    MESH_RETURN = MeshReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MESH_RETURN
