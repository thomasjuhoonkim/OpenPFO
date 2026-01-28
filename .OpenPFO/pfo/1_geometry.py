# classes
from classes.functions import GeometryParameters, GeometryReturn


def geometry(
    create_geometry_parameters: GeometryParameters,
) -> GeometryReturn:
    """
    This function is used to generate the geometry for each point in the design space.
    """

    assets_directory = create_geometry_parameters.output_assets_directory
    processors_per_job = create_geometry_parameters.processors_per_job
    job_id = create_geometry_parameters.job_id
    logger = create_geometry_parameters.logger
    point = create_geometry_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    GEOMETRY_RETURN = GeometryReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return GEOMETRY_RETURN
