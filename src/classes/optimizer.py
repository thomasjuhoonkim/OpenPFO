from constants.optimizer import AbstractOptimizer


class NoOptimizer(AbstractOptimizer):
    def __init__(self):
        pass

    def refine(self):
        pass

    def is_terminal(self, data):
        pass


class BayesianOptimizer(AbstractOptimizer):
    def __init__(self):
        pass

    def refine(self, objective_function):
        pass

    def is_terminal(self, data):
        pass


class NSGA2(AbstractOptimizer):
    def __init__(self):
        pass

    def refine(self, objective_function):
        pass

    def is_terminal(self, data):
        pass
