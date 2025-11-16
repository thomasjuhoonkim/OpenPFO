# subprocess
import subprocess

# util
from util.get_logger import get_logger

logger = get_logger()


def extract_assets(foam_filepath: str, output_assets_directory: str):
    """
    The extract_assets function is used to add side effects to your optimization
    workflow such as image extractation and data analysis. The extract_assets
    function runs AFTER the job and the objective extraction is ran for each
    grid point in the design space.

    All data from this function will be available to export after the full
    workflow has completed. You may store any data from this function in the
    provided side effects output directory.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    PVPYTHON = "/Applications/ParaView-6.0.1.app/Contents/bin/pvpython"
    PVSCRIPT = "/Users/thomaskim/Code/OpenPFO/input/pvbatch.py"
    command = [PVPYTHON, PVSCRIPT, foam_filepath, output_assets_directory]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logger.info(f"Output for command {command}: {result.stdout}")
    except subprocess.CalledProcessError as error:
        logger.error(f"{' '.join(command)} failed")
        logger.error(f"\n{error.stderr}")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
