# classes
from classes.functions import CreateGeometryParameters, CreateGeometryReturn


def create_geometry(
    create_geometry_parameters: CreateGeometryParameters,
) -> CreateGeometryReturn:
    """
    The create_geometry function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function does not return a value.
    """

    assets_directory = create_geometry_parameters.output_assets_directory
    processors_per_job = create_geometry_parameters.processors_per_job
    job_id = create_geometry_parameters.job_id
    logger = create_geometry_parameters.logger
    point = create_geometry_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    CREATE_GEOMETRY_RETURN = CreateGeometryReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_GEOMETRY_RETURN
