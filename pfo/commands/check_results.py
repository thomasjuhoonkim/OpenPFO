# system
import os

# json
import json

# constants
from constants.path import OUTPUT_RESULTS_JSON

# util
from util.validate_results import validate_results
from util.get_logger import get_logger

logger = get_logger()


def check_results():
    if not os.path.isfile(OUTPUT_RESULTS_JSON):
        logger.error(f"{OUTPUT_RESULTS_JSON} does not exist")

    results = None
    with open(OUTPUT_RESULTS_JSON, "r") as json_file:
        results = json.load(json_file)

    # validate_results simply exists rather than returning a boolean
    validate_results(results=results)

    logger.info("All results checked successfully")
