from typing import Callable, List

import numpy as np
from numpy.random import RandomState

from heuristic.classes import Route, Solution
from heuristic.handling_mdp import MDP


class LocalSearch:

    def __init__(self):
        self.operators: List[Callable[..., Solution]] = []

    def add_operator(self, operator: Callable):
        self.operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        return current
        def improve(solution):
            for operator in self.operators:
                new_solution = operator(solution, rnd_state)

                if new_solution.objective() < solution.objective():
                    return improve(new_solution)

            return solution

        improved = improve(current.copy())

        for route in improved.routes:  # TODO when should we do this?
            self._apply_mdp(route)

        assert improved.objective() <= current.objective()
        return improved

    @staticmethod
    def _apply_mdp(route: Route):
        if np.isclose(route.handling_cost(), 0.):
            return  # we cannot improve upon this.

        plan = MDP.from_route(route).solve()

        before = route.handling_cost()
        after = Route(route.customers, plan).handling_cost()

        if before < after:
            # Even with an MDP, this can happen as we implicitly assume
            # an equal number of blocks are assigned to each stack. That
            # is not always optimal, hence this check.
            return

        route.plan = plan
        route.invalidate_handling_cache()
