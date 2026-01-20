# system
import shutil

# constants
from constants.path import OUTPUT_DIRECTORY

# util
from util.get_logger import get_logger

logger = get_logger()


def reset_output():
    logger.warning(f"{OUTPUT_DIRECTORY} directory exists, removing it...")

    shutil.rmtree(OUTPUT_DIRECTORY)

    logger.info(f"{OUTPUT_DIRECTORY} directory was reset")

    return None
