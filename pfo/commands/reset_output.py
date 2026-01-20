# system
import os
import shutil

# constants
from constants.path import OUTPUT_DIRECTORY

# util
from util.get_logger import get_logger

logger = get_logger()


def reset_output():
    if os.path.isdir(OUTPUT_DIRECTORY):
        logger.warning(f"{OUTPUT_DIRECTORY} directory exists, removing it...")
        shutil.rmtree(OUTPUT_DIRECTORY)
        logger.info(f"{OUTPUT_DIRECTORY} directory was reset")
    else:
        logger.warning(f"{OUTPUT_DIRECTORY} does not exist, reset not necessary")

    return None
