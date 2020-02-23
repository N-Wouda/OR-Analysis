from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import remove_empty_routes


@remove_empty_routes
def worst_removal(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    return current
