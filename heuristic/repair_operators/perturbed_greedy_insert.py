from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.constants import MIN_OFFSET
from ._yth_best_insert import _yth_best_insert


def perturbed_greedy_insert(current: Solution,
                            rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into their y-th best, feasible route at a locally optimal leg of the tour.

    Perturbed sequential best insertion in Hornstra et al. (2020).
    """

    return _yth_best_insert(MIN_OFFSET, current, rnd_state)
