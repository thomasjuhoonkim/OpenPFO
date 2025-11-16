# classes
from classes.modeler import FreeCADModeler, OpenVSOModeler

# constants
from constants.modeler import EModeler


def get_modeler(modeler: EModeler):
    match modeler:
        case EModeler.FREECAD:
            return FreeCADModeler()
        case EModeler.OPENVSP:
            return OpenVSOModeler()
