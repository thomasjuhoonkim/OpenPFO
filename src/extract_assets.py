# system
import subprocess

# classes
from classes.functions import ExtractAssetsParameters


def extract_assets(extract_assets_parameters: ExtractAssetsParameters):
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

    PVPYTHON = "/Applications/ParaView-6.0.1.app/Contents/bin/pvpython"
    PVSCRIPT = "/Users/thomaskim/Code/OpenPFO/input/pvbatch.py"
    command = [
        PVPYTHON,
        PVSCRIPT,
        extract_assets_parameters.output_case_foam_filepath,
        extract_assets_parameters.output_assets_directory,
    ]

    logger = extract_assets_parameters.logger
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        logger.info(
            f"Extracted assets into {extract_assets_parameters.output_assets_directory}"
        )
    except subprocess.CalledProcessError as error:
        logger.error(f"{' '.join(command)} failed")
        logger.error(f"\n{error.stderr}")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
