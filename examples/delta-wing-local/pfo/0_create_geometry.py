# classes
from classes.functions import CreateGeometryParameters, CreateGeometryReturn
from classes.modeler import OpenVSPModeler
from classes.point import Point
from classes.variable import Variable


def create_geometry(
    create_geometry_parameters: CreateGeometryParameters,
) -> CreateGeometryReturn:
    """
    The create_geometry function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function returns the geometry filepath.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    # destructure parameters
    job_id = create_geometry_parameters.job_id
    point = create_geometry_parameters.grid_point
    output_assets_directory = create_geometry_parameters.output_assets_directory

    # OpenVSP
    OPENVSP_FILEPATH = "/Users/thomaskim/Downloads/OpenVSP-3.46.0-MacOS/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"

    openvsp_modeler = OpenVSPModeler(
        model_filepath=MODEL_FILEPATH, openvsp_filepath=OPENVSP_FILEPATH
    )
    openvsp_modeler.check_model()

    root_chord_variable = point.get_variables()[0]
    root_chord = root_chord_variable.get_value()
    tip_chord = 0.10  # metres
    taper_ratio = tip_chord / root_chord
    sweep = 2253.36 * taper_ratio**2 - 730.13 * taper_ratio + 79.72
    sweep_variable = Variable(
        name="Sweep", id="DFMNISRTXAJ:WingGeom:XSec_1:Sweep", value=sweep
    )
    updated_variables = [*point.get_variables(), sweep_variable]
    updated_point = Point(updated_variables)

    output_geometry_filepath = openvsp_modeler.generate_geometry(
        job_id=job_id,
        point=updated_point,
        output_assets_directory=output_assets_directory,
    )

    CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
        output_geometry_filepath=output_geometry_filepath,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_GEOMETRY_RETURN
