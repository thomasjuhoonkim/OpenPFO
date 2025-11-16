# util
from util.get_logger import get_logger
from util.get_modeler import get_modeler

# ==============================================================================

logger = get_logger()


def check_model():
    modeler = get_modeler()
    modeler.check_model()

    logger.info("Model is valid")
