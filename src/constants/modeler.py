from abc import ABC, abstractmethod
from enum import Enum

# classes
from classes.point import Point


class AbstractModeler(ABC):
    @abstractmethod
    def check_model(self):
        pass

    @abstractmethod
    def generate_geometry(self, job_id: str, point: Point):
        pass


class EModeler(Enum):
    FREECAD = "freecad"
    OPENVSP = "openvsp"
