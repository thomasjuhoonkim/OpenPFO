from abc import ABC, abstractmethod

# classes
from classes.point import Point


class AbstractModeler(ABC):
    @abstractmethod
    def check_model(self):
        pass

    @abstractmethod
    def generate_geometry(self, job_id: str, point: Point):
        pass
