from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customer_handling_costs
from ._worst import _worst


def worst_handling(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    costs = customer_handling_costs(current)
    return _worst(costs, current, rnd_state)
