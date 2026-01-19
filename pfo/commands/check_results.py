# classes
from classes.progress import Progress

# constants
from constants.path import OUTPUT_RESULTS_JSON

# util
from util.get_logger import get_logger

logger = get_logger()


def check_results():
    Progress(results_json_filepath=OUTPUT_RESULTS_JSON)

    return None
