from numpy.random import Generator

from heuristic.classes import Solution
from heuristic.functions import handling_costs
from ._worst import _worst


def worst_handling(current: Solution, rnd_state: Generator) -> Solution:
    """
    Randomly removes customers based on their handling cost, the additional
    handling cost of having said customer in the solution. The random sample is
    skewed to favour removing worst-cost customers.

    Similar to worst handling removal in Hornstra et al. (2020).
    """
    return _worst(handling_costs(current), current, rnd_state)
