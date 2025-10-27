def objective_function(something) -> float:
    """
    The objective function is used to rank simulation results in a single or
    multi-objective optimization case. Objective functions vary for every
    problem and must be carefully designed and tuned for the needs of the user.

    The objective function MUST process OpenFOAM results for each grid point in
    the design space using a post-processor of your choice.

    This objective function MUST return a single floating point value
    (objective_value), please reassign this value in your code. The units of the
    value do not matter as the comparison between grid points in the design
    space are relative.

    Optionally, you can add side effects to your optimization such as image
    extractation and data analysis using inputs/side_effects.py
    """

    objective_value = 0

    """ ======================= YOUR CODE BELOW HERE ======================= """

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return objective_value
