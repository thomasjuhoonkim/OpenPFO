# classes
from classes.modeler import FreeCADModeler, OpenVSOModeler

# constants
from constants.modeler import EModeler

# util
from util.get_config import get_config
from util.get_logger import get_logger

logger = get_logger()
config = get_config()

MODELER = config["model"]["type"]


def get_modeler():
    match MODELER:
        case EModeler.FREECAD:
            return FreeCADModeler()
        case EModeler.OPENVSP:
            return OpenVSOModeler()
        case _:
            raise RuntimeError("No matching modeler found")
