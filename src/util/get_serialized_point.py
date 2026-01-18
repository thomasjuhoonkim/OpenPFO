from classes.point import Point


def get_serialized_point(point: Point):
    variables = point.get_variables()
    return [
        {
            "id": variable.get_id(),
            "name": variable.get_name(),
            "value": variable.get_value(),
        }
        for variable in variables
    ]
