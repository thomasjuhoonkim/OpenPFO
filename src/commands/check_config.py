# system
import sys

# util
from util.get_config import get_config
from util.get_logger import get_logger

logger = get_logger()
config = get_config()


def check_config():
    # compute
    if "compute" not in config:
        logger.error("[compute] is missing")
        sys.exit(1)
    if "processors" not in config["compute"]:
        logger.error("processors is missing from [compute]")
        sys.exit(1)
    if not isinstance(config["compute"]["processors"], int):
        logger.error("processors is not an integer")
        sys.exit(1)

    # model
    if "model" not in config:
        logger.error("[model] is missing")
        sys.exit(1)
    if "parameters" not in config["model"]:
        logger.error("[[model.parameters]] is missing from [model]")
        sys.exit(1)
    if not isinstance(config["model"]["parameters"], list):
        logger.error("[[model.parameters]] is not a list")
        sys.exit(1)
    for parameter in config["model"]["parameters"]:
        attribtutes = [("id", str), ("name", str), ("min", float), ("max", float)]
        for attribute in attribtutes:
            field, type = attribute
            if not isinstance(parameter[field], type):
                logger.error(f'"{field}" in [[model.parameters]] is not {type}')
                sys.exit(1)

    if "optimizer" not in config:
        logger.error("[optimizer] is missing")
        sys.exit(1)
    if "objectives" not in config["optimizer"]:
        logger.error("[[optimizer.objectives]] is missing from [optimizer]")
        sys.exit(1)
    if not isinstance(config["optimizer"]["objectives"], list):
        logger.error("[[optimizer.objectives]] is not a list")
        sys.exit(1)
    for objective in config["optimizer"]["objectives"]:
        attribtutes = [("id", str), ("name", str), ("type", str)]
        for attribute in attribtutes:
            field, type = attribute
            if not isinstance(objective[field], type):
                logger.error(f'"{field}" in [[optimizer.objectives]] is not {type}')
                sys.exit(1)

    logger.info("Config is valid")

    return None
