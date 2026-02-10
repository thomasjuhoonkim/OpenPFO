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

    root_chord_variable = point.get_variables()[0]
    root_chord = root_chord_variable.get_value()
    tip_chord = 0.10  # metres
    taper_ratio = tip_chord / root_chord
    sweep = 2274.36 * taper_ratio**2 - 687.62 * taper_ratio + 68.69
    sweep_variable = Variable(
        name="Sweep", id="DFMNISRTXAJ:WingGeom:XSec_1:Sweep", value=sweep
    )
    updated_variables = [*point.get_variables(), sweep_variable]
    updated_point = Point(variables=updated_variables)

    # ==========================================================================

    # OpenVSP
    OPENVSP_FILEPATH = "/home/tkim/scratch/OpenVSP/build/vsp/vspscript"
    MODEL_FILEPATH = "input/model.vsp3"
    STL_FILEPATH = f"{job_directory}/{job_id}.stl"
    VSPSCRIPT_FILEPATH = f"{job_directory}/{job_id}.vspscript"
    DES_FILEPATH = f"{job_directory}/{job_id}.des"
    POINT = updated_point

    # design variables file for openvsp model variable definitions
    variables = POINT.get_variables()
    variables_definitions = ""

    for variable in variables:
        id = variable.get_id()
        value = variable.get_value()
        variables_definitions += f"{id}: {value}\n"
    design_variables_content = f"""{len(variables)}\n{variables_definitions}"""

    with open(DES_FILEPATH, "w") as f:
        f.write(design_variables_content)

    # vspscript file for vsp model mutation
    vspscript_content = f"""
void main()
{{
    ClearVSPModel();
    ReadVSPFile("{MODEL_FILEPATH}");
    Update();
    ReadApplyDESFile("{DES_FILEPATH}");
    Update();
    ExportFile("{STL_FILEPATH}", SET_ALL, EXPORT_STL);
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

    GEOMETRY_RETURN = GeometryReturn(visualize_filepath=STL_FILEPATH)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return GEOMETRY_RETURN
