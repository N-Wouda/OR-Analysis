from itertools import product
from typing import List

import numpy as np

from heuristic.classes import Stacks
from .MDP import MDP


def solve(mdp: MDP) -> List[Stacks]:
    """
    Determines an optimal loading plan in blocks for each leg of the MDP's
    route. O(|customers| * NUM_BLOCKS!), where customers are the customers in
    the MDP's route.
    """
    costs = np.empty((len(mdp.legs), len(mdp.states)))
    costs[-1, :] = 0.

    decisions = np.empty((len(mdp.legs) - 1, len(mdp.states)), dtype=int)
    leg_cost = np.empty((len(mdp.states), len(mdp.states)))

    for next_customer in range(len(mdp.legs) - 1, 0, -1):
        curr_customer = next_customer - 1

        for from_state, to_state in product(range(len(mdp.states)), repeat=2):
            next_cost = costs[next_customer, to_state]

            # Current cost is the cost made for leaving the current customer
            # with from_state, and leaving the next customer with to_state.
            curr_cost = mdp.cost(mdp.legs[next_customer],
                                 mdp.states[from_state],
                                 mdp.states[to_state])

            leg_cost[from_state, to_state] = curr_cost + next_cost

        costs[curr_customer, :] = np.min(leg_cost, axis=1)
        decisions[curr_customer, :] = np.argmin(leg_cost, axis=1)

    return mdp.plan(costs, decisions)
