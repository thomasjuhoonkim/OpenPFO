# system
import os
import shutil

# constants
from constants.path import (
    OUTPUT_CASES_DIRECTORY,
    OUTPUT_DIRECTORY,
    OUTPUT_ASSETS_DIRECTORY,
)

# util
from util.get_logger import get_logger

# ==============================================================================

# logging
logger = get_logger()


def reset_output():
    # check if output directory exists
    if not os.path.isdir(OUTPUT_DIRECTORY):
        logger.warning(f"{OUTPUT_DIRECTORY} directory does not exist, creating one...")
        os.makedir(OUTPUT_DIRECTORY)

    subdirectories = [
        OUTPUT_CASES_DIRECTORY,
        OUTPUT_ASSETS_DIRECTORY,
    ]
    for directory in subdirectories:
        # create directory if it does not exist
        if not os.path.isdir(directory):
            logger.warning(f"{directory} directory does not exist, creating one...")
            os.mkdir(directory)

        # check if directory are empty
        if os.listdir(directory):
            logger.warning(f"Found items under {directory}, removing them...")
            shutil.rmtree(directory)
            os.mkdir(directory)

    logger.info("Output directory was reset")
