from classes.optimizer import Optimizer


class NoOptimizer(Optimizer):
    def __init__(self):
        pass

    def refine(self, objective_function):
        pass


class BayesianOptimizer(Optimizer):
    def __init__(self, multi_objective: bool):
        pass

    def refine(self, objective_function):
        pass


class GeneticOptimizer(Optimizer):
    def __init__(self, multi_objective: bool, multi_region: bool):
        pass

    def refine(self, objective_function):
        pass
