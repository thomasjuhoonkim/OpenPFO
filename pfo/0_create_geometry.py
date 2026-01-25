# classes
from classes.functions import CreateGeometryParameters, CreateGeometryReturn
from classes.modeler import FreeCADModeler, OpenVSPModeler
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
    point = create_geometry_parameters.point
    output_assets_directory = create_geometry_parameters.output_assets_directory

    # OpenVSP
    OPENVSP_FILEPATH = "/home/tkim/scratch/OpenVSP/build/vsp/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"

    openvsp_modeler = OpenVSPModeler(
        model_filepath=MODEL_FILEPATH, openvsp_filepath=OPENVSP_FILEPATH
    )
    openvsp_modeler.check_model()

    output_geometry_filepath = openvsp_modeler.generate_geometry(
        job_id=job_id,
        point=point,
        output_assets_directory=output_assets_directory,
    )

    CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
        output_geometry_filepath=output_geometry_filepath,
    )

    # ==========================================================================

    # # destructure parameters
    # point = create_geometry_parameters.point
    # job_id = create_geometry_parameters.job_id
    # output_assets_directory = create_geometry_parameters.output_assets_directory

    # FreeCAD
    # MODEL_FILEPATH = "input/model.FCStd"
    # FREECAD_FILEPATH = "/Applications/FreeCAD.app/Contents/Resources/lib"
    # # FREECAD_FILEPATH = "/usr/lib/freecad/lib"
    # # FREECAD_FILEPATH = "C:\\Program Files\\FreeCAD\\bin"
    # freecad_modeler = FreeCADModeler(
    #     model_filepath=MODEL_FILEPATH, freecad_filepath=FREECAD_FILEPATH
    # )
    # freecad_modeler.check_model()

    # output_geometry_filepath = freecad_modeler.generate_geometry(
    #     job_id=job_id,
    #     point=point,
    #     output_assets_directory=output_assets_directory,
    # )

    # CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
    #     output_geometry_filepath=output_geometry_filepath
    # )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_GEOMETRY_RETURN
