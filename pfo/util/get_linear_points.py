# classes
from classes.point import Point
from classes.variable import Variable

# util
from util.get_config_parameters import get_config_parameters


def get_linear_points(count: int):
    parameters = get_config_parameters()

    points = []
    for i in range(count):
        variables = []
        for parameter in parameters:
            lower_bound = parameter.get_min()
            upper_bound = parameter.get_max()
            # Calculate equally spaced value
            step = (upper_bound - lower_bound) / (count - 1)
            value = lower_bound + step * i

            variable = Variable(
                name=parameter.get_name(), id=parameter.get_id(), value=value
            )
            variables.append(variable)

        point = Point(variables)
        points.append(point)

    return points
