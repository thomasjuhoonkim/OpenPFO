# system
import os
import sys

# constants
from constants.path import (
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_CASES_DIRECTORY,
    OUTPUT_DIRECTORY,
)
from util.get_logger import get_logger

logger = get_logger()


def check_output():
    # check if output directory exists
    if not os.path.isdir(OUTPUT_DIRECTORY):
        logger.warning(
            f"{OUTPUT_DIRECTORY} directory does not exist, run `pfo resetOutput`"
        )
        sys.exit(1)

    directories = [OUTPUT_CASES_DIRECTORY, OUTPUT_ASSETS_DIRECTORY]
    for directory in directories:
        # check if output directories exist
        if not os.path.isdir(directory):
            logger.warning(
                f"{directory} directory does not exist, run `pfo resetOutput`"
            )

        # check if output directories have content
        if os.listdir(directory):
            logger.warning(
                f"Found items under {directory}, please save them or run `pfo resetOutput`"
            )
            sys.exit(1)

    logger.info("Output directory is valid")
