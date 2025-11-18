# logging
import logging
import coloredlogs

LOGGER_NAME = "OpenPFO"
FILENAME = "OpenPFO.log"
FILEMODE = "w"
LEVEL = logging.INFO
FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

# file logs
logging.basicConfig(filename=FILENAME, filemode=FILEMODE, level=LEVEL, format=FORMAT)

# color logs
coloredlogs.install(level=LEVEL, fmt=FORMAT)
