# constants
from constants.cli import MODELER_ARGUMENT
from constants.modeler import EModeler

# util
from util.get_logger import get_logger
from util.get_modeler import get_modeler

# ==============================================================================

logger = get_logger()


def check_model(modeler: EModeler = MODELER_ARGUMENT):
    runtime_modeler = get_modeler(modeler=modeler)
    runtime_modeler.check_model()

    logger.info("Model is valid")
