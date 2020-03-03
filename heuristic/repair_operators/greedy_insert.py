from numpy.random import RandomState

from heuristic.classes import Solution
from ._random_near_best_greedy_insert import _random_near_best_greedy_insert


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their best, feasible route at a locally optimal leg of the tour.

    Sequential best insertion in Hornstra et al. (2020).
    """
    return _random_near_best_greedy_insert(1, current, rnd_state)
