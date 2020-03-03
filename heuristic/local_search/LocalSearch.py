from typing import Callable, List

import numpy as np
from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.constants import DEPOT
from heuristic.handling_mdp import get_mdp, solve


class LocalSearch:

    def __init__(self):
        self.operators: List[Callable[..., Solution]] = []

    def add_operator(self, operator: Callable):
        self.operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = current.copy()

        for route in improved.routes:
            if np.isclose(route.handling_cost(), 0.):
                continue  # we cannot improve upon this.

            mdp = get_mdp(route)
            costs, decisions = solve(mdp)

            layouts = []

            for idx, customer in enumerate(mdp.customers):
                if idx == 0:
                    layouts.append(np.argmin(costs[idx, :]).item())
                    continue

                layouts.append(decisions[idx - 1, layouts[-1]])

            plan = []

            for idx, layout in enumerate(layouts):
                state = mdp.states[layout]

                if idx == 0:
                    stacks = mdp.stacks_from_state(state, DEPOT, False)
                else:
                    stacks = mdp.stacks_from_state(state, mdp.customers[idx],
                                                   True)

                plan.append(stacks)

            route.plan = plan
            route._handling_cost = None

        return improved
