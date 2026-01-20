# classes
from classes.progress import Progress

# util
from util.get_logger import get_logger

logger = get_logger()


def check_results():
    Progress(resume=True)

    return None
