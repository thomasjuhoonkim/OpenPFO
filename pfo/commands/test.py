from classes.modeler import OpenVSPModeler
from classes.variable import Variable
from classes.point import Point


def test():
    # destructure parameters
    variable = Variable(
        name="Root Chord", id="GFXAORPLFWH:WingGeom:XSec_1:Root_Chord", value=1.2
    )
    point = Point(variables=[variable])
    job_id = "test-1"
    output_assets_directory = "output"

    # OpenVSP
    OPENVSP_FILEPATH = "/home/tkim/scratch/OpenVSP/build/vsp"
    # OPENVSP_FILEPATH = "/Users/thomaskim/Downloads/OpenVSP-3.46.0-MacOS/vspscript"
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

    print(output_geometry_filepath)
