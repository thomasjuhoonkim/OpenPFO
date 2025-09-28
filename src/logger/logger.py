# logging
import logging
import coloredlogs

LOGGER_NAME = "OpenPFO_Logger"

# logging
coloredlogs.install(level=logging.DEBUG)
# coloredlogs.install(level=logging.INFO)
logger = logging.getLogger(LOGGER_NAME)
