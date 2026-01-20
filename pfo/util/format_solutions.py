# classes
from classes.solution import Solution


def format_solutions(solutions: list["Solution"]):
    solution_representations = [
        f"SOLUTION {i}\n{solution.get_solution_representation()}"
        for i, solution in enumerate(solutions)
    ]
    return "\n" + "\n\n".join(solution_representations)
