from typing import List

import numpy as np

from heuristic.classes import Stacks


def get_plan(mdp, costs, decisions) -> List[Stacks]:
    layouts = [np.argmin(costs[0, :])]

    for idx, _ in enumerate(mdp.route.customers):
        layouts.append(decisions[idx, layouts[-1]])

    plan = []

    for idx, layout in enumerate(layouts):
        state = mdp.states[layout]

        # When idx == 0 we are at the depot, and we do not have
        # anything to unload (so these are all demands).
        stacks = mdp.state_to_stacks(state, mdp.legs[idx], idx != 0)
        plan.append(stacks)

    return plan
