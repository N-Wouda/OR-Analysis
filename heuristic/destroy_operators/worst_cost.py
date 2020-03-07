from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import handling_costs, routing_costs
from ._worst import _worst


def worst_cost(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes customers based on their cost: the additional routing and
    handling costs of having said customer in the solution. The random sample
    is skewed to favour removing worst-cost customers.

    Similar to worst removal in Hornstra et al. (2020).
    """
    return _worst(routing_costs(current) + handling_costs(current),
                  current,
                  rnd_state)
