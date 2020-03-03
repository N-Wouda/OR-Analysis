from numpy.random import RandomState

from heuristic.classes import Solution
from ._yth_best_insert import _yth_best_insert


def greedy_insert(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their best, feasible route at a locally optimal leg of the tour.

    Sequential best insertion in Hornstra et al. (2020).
    """
    return _yth_best_insert(1, current, rnd_state)
