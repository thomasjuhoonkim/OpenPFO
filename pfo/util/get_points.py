# classes
from classes.point import Point
from classes.variable import Variable

# util
from util.get_config_parameters import get_config_parameters


def get_point(coordinates: list[float]):
    parameters = get_config_parameters()

    variables = []
    for i, coordinate in enumerate(coordinates):
        variable = Variable(
            name=parameters[i].get_name(),
            id=parameters[i].get_id(),
            value=coordinate,
        )
        variables.append(variable)

    return Point(variables=variables)
