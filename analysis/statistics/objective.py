from typing import Tuple

from heuristic.classes import Solution


def objective(solution: Solution) -> Tuple[str, float]:
    """
    Returns Solution objective.
    """
    return "objective", solution.objective()
