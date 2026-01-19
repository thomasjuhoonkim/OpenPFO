from classes.parameter import Parameter


def get_serialized_parameter(parameter: Parameter):
    return {
        "id": parameter.get_id(),
        "name": parameter.get_name(),
        "min": parameter.get_min(),
        "max": parameter.get_max(),
        "value": parameter.get_value(),
    }
