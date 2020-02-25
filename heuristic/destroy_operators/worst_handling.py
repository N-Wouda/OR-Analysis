from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import customer_handling_costs
from ._worst import _worst


def worst_handling(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes customers based on their handling cost, the additional
    handling cost of having said customer in the solution. The random sample is
    skewed to favour removing worst-cost customers.

    Similar to worst handling removal in Hornstra et al. (2020).
    """
    costs = customer_handling_costs(current)
    return _worst(costs, current, rnd_state)
