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
    to_remove = customers_to_remove(problem.num_customers)

    # If this is really slow we can use Gauss to remove the normalisation.
    probabilities = np.arange(problem.num_customers, 0, -1)
    probabilities = probabilities / np.sum(probabilities)

    return rnd_state.choice(np.arange(problem.num_customers),
                            to_remove,
                            replace=False,
                            p=probabilities)
