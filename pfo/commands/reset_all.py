# commands
from commands.reset_case_template import reset_case_template
from commands.reset_output import reset_output

# util
from util.get_logger import get_logger

logger = get_logger()


def reset_all():
    reset_case_template()
    reset_output()

    logger.info("Input and output directories were reset")
