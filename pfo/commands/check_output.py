# system
import os
import sys

# constants
from constants.path import OUTPUT_DIRECTORY

# util
from util.get_logger import get_logger

logger = get_logger()


def check_output():
    # check if output directory exists
    if os.path.isdir(OUTPUT_DIRECTORY):
        logger.warning(
            f"{OUTPUT_DIRECTORY} directory already exists, make sure you run `pfo resetOutput` or specify the --resume flag to resume a run"
        )
        sys.exit(1)

    os.makedirs(OUTPUT_DIRECTORY)

    logger.info(f"{OUTPUT_DIRECTORY} directory is valid")
