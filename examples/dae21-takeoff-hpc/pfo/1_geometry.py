# system
import subprocess

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

    # ==========================================================================

    # OpenVSP
    OPENVSP_FILEPATH = "/home/tkim/scratch/OpenVSP/build/vsp/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"
    STL_FILEPATH = f"{job_directory}/{job_id}.stl"
    VSPSCRIPT_FILEPATH = f"{job_directory}/{job_id}.vspscript"
    INPUT_DES_FILEPATH = f"{job_directory}/{job_id}-input.des"
    OUTPUT_DES_FILEPATH = f"{job_directory}/{job_id}-output.des"

    # design variables file for openvsp model variable definitions
    variables = point.get_variables()
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
