# system
import shutil
import os

# constants
from constants.path import INPUT_CASE_TEMPLATE, INPUT_DIRECTORY, OPENPFO_CASE_TEMPLATE

# OpenFOAM
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory

# util
from util.get_logger import get_logger

# ==============================================================================

# logging
logger = get_logger()


def reset_case_template():
    # check if input directory exists
    if not os.path.isdir(INPUT_DIRECTORY):
        logger.warning(f"{INPUT_DIRECTORY} directory does not exist, creating one...")
        os.makedir(INPUT_DIRECTORY)

    # create directory if it does not exist
    if not os.path.isdir(INPUT_CASE_TEMPLATE):
        logger.warning(
            f"{INPUT_CASE_TEMPLATE} directory does not exist, creating one..."
        )

    # check if input case template directory is empty
    if os.listdir(INPUT_CASE_TEMPLATE):
        logger.warning(f"Found items under {INPUT_CASE_TEMPLATE}, removing them...")
        shutil.rmtree(INPUT_CASE_TEMPLATE)
        os.mkdir(INPUT_CASE_TEMPLATE)

    # copy OpenPFO template case to input template case
    base_case = SolutionDirectory(OPENPFO_CASE_TEMPLATE)
    copy_case = base_case.cloneCase(INPUT_CASE_TEMPLATE)
    logger.info(f"Copied OpenFOAM case {copy_case.name} in ./{INPUT_CASE_TEMPLATE}")

    logger.info("Input case template was reset")
