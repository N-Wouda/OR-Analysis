from itertools import product
from typing import Tuple

import numpy as np

from .MDP import MDP


def solve(mdp: MDP) -> Tuple[np.ndarray, np.ndarray]:
    """
    Determines an optimal block assignment for each leg of the MDP's route.
    O(|customers| * NUM_BLOCKS!), where customers are the customers in the
    MDP's route.
    """
    costs = np.empty((len(mdp.legs), len(mdp.states)))
    costs[-1, :] = 0.

    decisions = np.empty((len(mdp.legs) - 1, len(mdp.states)), dtype=int)

    leg_cost = np.empty((len(mdp.states), len(mdp.states)))

    for next_customer in range(len(mdp.legs) - 1, 0, -1):
        current_customer = next_customer - 1

        for from_state, to_state in product(range(len(mdp.states)), repeat=2):
            next_cost = costs[next_customer, to_state]

            # Current cost is the cost made for leaving the current customer
            # with from_state, and leaving the next customer with to_state.
            # TODO check this carefully.
            curr_cost = mdp.cost(mdp.legs[next_customer],
                                 mdp.states[from_state],
                                 mdp.states[to_state])

            leg_cost[from_state, to_state] = curr_cost + next_cost

        costs[current_customer, :] = np.min(leg_cost, axis=1)
        decisions[current_customer, :] = np.argmin(leg_cost, axis=1)

    return costs, decisions
