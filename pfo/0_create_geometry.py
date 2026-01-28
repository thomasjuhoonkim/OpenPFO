# classes
from classes.functions import CreateGeometryParameters, CreateGeometryReturn


def create_geometry(
    create_geometry_parameters: CreateGeometryParameters,
) -> CreateGeometryReturn:
    """
    The create_geometry function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function returns the geometry filepath.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
        output_geometry_filepath="",
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_GEOMETRY_RETURN
