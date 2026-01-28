# random
import random

# classes
from classes.point import Point
from classes.variable import Variable

# util
from util.get_config_parameters import get_config_parameters


def get_random_points(count: int):
    parameters = get_config_parameters()

    points = []
    for _ in range(count):
        variables = []
        for parameter in parameters:
            lower_bound = parameter.get_min()
            upper_bound = parameter.get_max()
            random_float = random.uniform(lower_bound, upper_bound)

            variable = Variable(
                name=parameter.get_name(), id=parameter.get_id(), value=random_float
            )
            variables.append(variable)

        point = Point(variables)
        points.append(point)

    return points
