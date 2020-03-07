from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.constants import NEARNESS
from ._near_best_insert import _near_best_insert


def perturbed_greedy_insert(current: Solution,
                            rnd_state: RandomState) -> Solution:
    """
    Sequentially inserts each a random permutation of the unassigned customers
    into a near-best feasible route at a locally optimal leg of the tour. This
    is controlled by the ``NEARNESS`` constant.

    Perturbed sequential best insertion in Hornstra et al. (2020).
    """
    return _near_best_insert(NEARNESS, current, rnd_state)
