# system
import sys
import os

# classes
from classes.functions import GeometryParameters, GeometryReturn


def geometry(
    geometry_parameters: GeometryParameters,
) -> GeometryReturn:
    """
    This function is used to generate the geometry for each point in the design space.
    """

    job_directory = geometry_parameters.job_directory
    processors_per_job = geometry_parameters.processors_per_job
    job_id = geometry_parameters.job_id
    logger = geometry_parameters.logger
    point = geometry_parameters.point
    meta = geometry_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    FREECAD_FILEPATH = "/Applications/FreeCAD.app/Contents/Resources/bin/python"
    MODEL_FILEPATH = "input/model.FCStd"
    sys.path.append(FREECAD_FILEPATH)

    # FreeCAD module
    import FreeCAD  # type: ignore  # noqa: E402
    import Mesh  # type: ignore # noqa: E402

    FreeCAD.Version()

    # Acquire document & part
    document = FreeCAD.open(MODEL_FILEPATH)
    part = document.getObject("Body")

    # Design Space Interface
    spreadsheet = document.getObject("Spreadsheet")
    for variable in point.get_variables():
        cell = variable.get_id()
        value = str(variable.get_value())
        spreadsheet.set(cell, value)

    # Recompute Model
    document.recompute()

    # Export to AST
    output_ast = f"{job_directory}/{job_id}.ast"
    output_stl = f"{job_directory}/{job_id}.stl"
    Mesh.export([part], output_ast)

    # rename AST to STL
    os.rename(src=output_ast, dst=output_stl)

    # export to FCStd
    output_fcstd = f"{job_directory}/{job_id}.FCStd"
    document.saveAs(output_fcstd)

    # ==========================================================================

    # meta
    meta.add_meta("geometry", f"{job_id}.stl")

    GEOMETRY_RETURN = GeometryReturn(visualize_filepath=output_stl)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return GEOMETRY_RETURN
