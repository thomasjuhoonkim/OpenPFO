from classes.optimizer import NoOptimizer
from constants.optimizer import EOptimizer


def get_optimizer(optimizer: EOptimizer):
    match optimizer:
        case EOptimizer.NO_OPTIMIZER:
            return NoOptimizer()
        # case EOptimizer.GENETIC_OPTIMIZER:
        #     return GeneticOptimizer()
        # case EOptimizer.BAYSIAN_OPTIMIZER:
        #     return BayesianOptimizer()
