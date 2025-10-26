def objective_function(something) -> float:
    """
    The objective function is used to rank simulation results in a single or
    multi-objective optimization case. Objective functions vary for every
    problem and must be carefully designed and tuned for the needs of the user.

    The objective function MUST process OpenFOAM results for each grid point in
    the design space using a post-processor of your choice.

    This objective function MUST return a single floating point value, the units
    of the value do not matter as the comparison between grid points in the
    design space are relative.
    """
    pass
