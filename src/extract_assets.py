# system
import subprocess

# classes
from classes.functions import ExtractAssetsParameters, ExtractAssetsReturn


def extract_assets(
    extract_assets_parameters: ExtractAssetsParameters,
) -> ExtractAssetsReturn:
    """
    The extract_assets function is used to add side effects to your optimization
    workflow such as image extractation and data analysis. The extract_assets
    function runs AFTER execute_solver and extract_objectives.

    All data from this function will be available to export after the full
    workflow has completed. You may store any data from this function in the
    provided assets output directory.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = extract_assets_parameters.output_case_foam_filepath
    output_directory = extract_assets_parameters.output_assets_directory
    logger = extract_assets_parameters.logger

    PVBATCH = "/Applications/ParaView-6.0.1.app/Contents/bin/pvbatch"

    commands = [
        f"{PVBATCH} input/paraview/slice.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/geometry.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/mesh.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/streamline.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/streamline-half.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/slice-velocity.py {case_directory} {output_directory}",
        f"{PVBATCH} input/paraview/slice-pressure.py {case_directory} {output_directory}",
    ]

    run_ok = True
    for command in commands:
        try:
            subprocess.run(
                command.split(" "), capture_output=True, text=True, check=True
            )
            logger.info(f"Successfully ran {command} for {case_directory}")
        except subprocess.CalledProcessError as error:
            run_ok = False
            logger.error(f"{command} failed")
            logger.error(f"\n{error.stderr}")

    EXTRACT_ASSETS_RETURN = ExtractAssetsReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_ASSETS_RETURN
