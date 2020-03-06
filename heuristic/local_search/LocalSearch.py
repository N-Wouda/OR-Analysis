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

            layouts = [np.argmin(costs[0, :])]

            for idx, _ in enumerate(route.customers):
                layouts.append(decisions[idx, layouts[-1]])

            plan = []

            for idx, layout in enumerate(layouts):
                state = mdp.states[layout]

                # When idx == 0 we're at the depot, and we do not have
                # anything to unload (so these are all demands).
                stacks = mdp.state_to_stacks(state, mdp.legs[idx], idx != 0)
                plan.append(stacks)

            route.plan = plan
            route._handling_cost = None

        assert improved.objective() <= current.objective()
        return improved
