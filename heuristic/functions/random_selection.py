import numpy as np
from numpy.random import RandomState

from heuristic.classes import Problem
from .customers_to_remove import customers_to_remove


def random_selection(rnd_state: RandomState) -> np.ndarray:
    """
    Implements a random selection mechanism, which selects random indices for
    a certain list of num_customers length (e.g., for a cost computation),
    favouring smaller indices.
    """
    problem = Problem()

    triangle = np.arange(customers_to_remove(), 0, -1)

    probabilities = np.ones(problem.num_customers)
    probabilities[:customers_to_remove()] = triangle
    probabilities = probabilities / np.sum(probabilities)

    return rnd_state.choice(problem.num_customers,
                            customers_to_remove(),
                            replace=False,
                            p=probabilities)
