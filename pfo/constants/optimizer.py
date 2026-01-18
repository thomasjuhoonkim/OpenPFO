from abc import ABC, abstractmethod
from enum import Enum
import numpy as np


class AbstractOptimizer(ABC):
    @abstractmethod
    def refine(
        self,
        objective_values: list[np.ndarray[np.float64, np.dtype[np.float64]]],
    ):
        pass

    @abstractmethod
    def is_terminal(self, data):
        pass


class EOptimizer(Enum):
    NO_OPTIMIZER = "no-optimizer"
    BAYSIAN_OPTIMIZER = "bayesian-optimizer"
    GENETIC_OPTIMIZER = "genetic-optimizer"
