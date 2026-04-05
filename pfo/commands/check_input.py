# system
import os

# constants
from constants.path import INPUT_DIRECTORY

# util
from util.get_logger import get_logger

logger = get_logger()


def check_input():
    # check if input directory exists
    if not os.path.isdir(INPUT_DIRECTORY):
        logger.warning(f"{INPUT_DIRECTORY} directory does not exist, creating one now")
        os.makedirs(INPUT_DIRECTORY)

    logger.info(f"{INPUT_DIRECTORY} directory is valid")
