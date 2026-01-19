# util
from util.validate_results import validate_config
from util.get_config import get_config
from util.get_logger import get_logger

logger = get_logger()
config = get_config()


def check_config():
    validate_config(config)
