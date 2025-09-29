from abc import ABC, abstractmethod


class Optimizer(ABC):
    @abstractmethod
    def refine(self, objective_function):
        pass

    @abstractmethod
    def check_terminal(self):
        pass
