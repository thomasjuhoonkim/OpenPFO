# logging
import logging
from logger.logger import LOGGER_NAME


def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    return logger
