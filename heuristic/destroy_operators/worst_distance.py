from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customer_routing_costs
from ._worst import _worst


def worst_distance(current: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    costs = customer_routing_costs(current)
    return _worst(costs, current, rnd_state)
