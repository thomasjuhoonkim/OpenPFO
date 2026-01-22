# classes
from classes.functions import ExtractAssetsParameters, ExtractAssetsReturn

# util
from util.run_parallel_commands import run_parallel_commands


def extract_assets(
    extract_assets_parameters: ExtractAssetsParameters,
):
    """
    The extract_assets function is used to add side effects to your optimization
    workflow such as image extractation and data analysis. The extract_assets
    function runs AFTER execute_solver and extract_objectives.

    All data from this function will be available to export after the full
    workflow has completed. You may store any data from this function in the
    provided assets output directory.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = extract_assets_parameters.output_case_foam_filepath
    output_directory = extract_assets_parameters.output_assets_directory
    processors_per_job = extract_assets_parameters.processors_per_job

    PVBATCH = "/Applications/ParaView-6.0.0.app/Contents/bin/pvbatch"

    commands = [
        f"{PVBATCH} input/paraview/slice.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/geometry.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/mesh.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/streamline.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/streamline-half.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/slice-velocity.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/slice-pressure.py {case_directory} {output_directory}",
    ]

    run_parallel_commands(commands=commands, max_workers=processors_per_job)

    EXTRACT_ASSETS_RETURN = ExtractAssetsReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_ASSETS_RETURN
