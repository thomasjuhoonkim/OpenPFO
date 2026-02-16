# system
import subprocess

# classes
from classes.functions import GeometryParameters, GeometryReturn
from classes.variable import Variable
from classes.point import Point


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
    root_chord = meta.get_meta("root-chord")
    root_chord_variable = Variable(
        name="Root Chord", id="GFXAORPLFWH:WingGeom:XSec_1:Root_Chord", value=root_chord
    )

    geometry_variables_excluding_ground_height = [*point.get_variables()]
    geometry_variables_excluding_ground_height.pop(-1)
    updated_geometry_variables = [
        *geometry_variables_excluding_ground_height,
        root_chord_variable,
    ]
    updated_point = Point(variables=updated_geometry_variables)

    # ==========================================================================

    # OpenVSP
    OPENVSP_FILEPATH = "/Users/thomaskim/Downloads/OpenVSP-3.46.0-MacOS/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"
    STL_FILEPATH = f"{job_directory}/{job_id}.stl"
    VSPSCRIPT_FILEPATH = f"{job_directory}/{job_id}.vspscript"
    INPUT_DES_FILEPATH = f"{job_directory}/{job_id}-input.des"
    OUTPUT_DES_FILEPATH = f"{job_directory}/{job_id}-output.des"
    POINT = updated_point

    # design variables file for openvsp model variable definitions
    variables = POINT.get_variables()
    variables_definitions = ""

    for variable in variables:
        id = variable.get_id()
        value = variable.get_value()
        variables_definitions += f"{id}: {value}\n"
    design_variables_content = f"""{len(variables)}\n{variables_definitions}"""

    with open(INPUT_DES_FILEPATH, "w") as f:
        f.write(design_variables_content)

    # vspscript file for vsp model mutation
    vspscript_content = f"""
void main()
{{
    ClearVSPModel();

    ReadVSPFile("{MODEL_FILEPATH}");
    Update();
    ReadApplyDESFile("{INPUT_DES_FILEPATH}");
    Update();
    ExportFile("{STL_FILEPATH}", SET_ALL, EXPORT_STL);

    DeleteAllDesignVars();
    string compGeomID = ComputeCompGeom(SET_ALL, false, 0);
    string resultID = FindLatestResultsID("Comp_Geom");
    double volume = GetDoubleResults(resultID, "Theo_Vol")[0];
    string volumeParameterID = AddUserParm(PARM_DOUBLE_TYPE, "Volume", "Design");
    SetParmVal(volumeParameterID, volume);
    AddDesignVar(volumeParameterID, 0);
    Update();
    WriteDESFile("{OUTPUT_DES_FILEPATH}");

    VSPExit(0);
}}
"""

    with open(VSPSCRIPT_FILEPATH, "w") as f:
        f.write(vspscript_content)

    # cli commands for openvsp
    command = [
        OPENVSP_FILEPATH,
        "-script",
        VSPSCRIPT_FILEPATH,
    ]

    subprocess.run(command, capture_output=True, text=True, check=True)
    logger.info(
        f"Generated {STL_FILEPATH}, design variables: {point.get_representation()}"
    )

    # ==========================================================================

    # volume extraction
    volume_value = None
    with open(OUTPUT_DES_FILEPATH, "r") as f:
        lines = f.readlines()
        line = lines[1]
        part = line.split(" ")[1]
        volume_value = float(part)

    # ==========================================================================

    # meta
    meta.add_meta("volume", volume_value)
    meta.add_meta("geometry", f"{job_id}.stl")

    GEOMETRY_RETURN = GeometryReturn(visualize_filepath=STL_FILEPATH)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return GEOMETRY_RETURN
