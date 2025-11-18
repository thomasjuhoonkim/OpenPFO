# classes
from classes.functions import CreateGeometryParameters, CreateGeometryReturn
from classes.modeler import FreeCADModeler, OpenVSOModeler


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

    # constants
    OPENVSP_FILEPATH = "/Users/thomaskim/Downloads/OpenVSP-3.46.0-MacOS/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"

    modeler = OpenVSOModeler(
        model_filepath=MODEL_FILEPATH, openvsp_filepath=OPENVSP_FILEPATH
    )
    modeler.check_model()
    output_geometry_filepath = modeler.generate_geometry(
        job_id=job_id, point=point, output_assets_directory=output_assets_directory
    )

    CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
        output_geometry_filepath=output_geometry_filepath
    )

    # ==========================================================================

    # destructure parameters
    # point = create_geometry_parameters.grid_point
    # job_id = create_geometry_parameters.job_id
    # output_assets_directory = create_geometry_parameters.output_assets_directory

    # SCALE_FACTOR = 0.001  # scale factor (1 mm -> 0.001 m)
    # MODEL_FILEPATH = "input/model.FCStd"
    # FREECAD_FILEPATH = "/Applications/FreeCAD.app/Contents/Resources/lib"
    # # FREECAD_FILEPATH = "/usr/lib/freecad/lib"
    # # FREECAD_FILEPATH = "C:\\Program Files\\FreeCAD\\bin"

    # modeler = FreeCADModeler(
    #     model_filepath=MODEL_FILEPATH, freecad_filepath=FREECAD_FILEPATH
    # )
    # modeler.check_model()
    # output_geometry_filepath = modeler.generate_geometry(
    #     job_id=job_id,
    #     point=point,
    #     scale_factor=SCALE_FACTOR,
    #     output_assets_directory=output_assets_directory,
    # )

    # CREATE_GEOMETRY_RETURN = CreateGeometryReturn(
    #     output_geometry_filepath=output_geometry_filepath
    # )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_GEOMETRY_RETURN
