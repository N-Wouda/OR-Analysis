from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.handling_mdp import get_mdp, solve


class LocalSearch:

    def __init__(self):
        self.operators: List[Callable[..., Solution]] = []

    def add_operator(self, operator: Callable):
        self.operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        improved = current.copy()

        for route in improved.routes:
            if len(route.customers) == 1:
                continue

            mdp = get_mdp(route)
            solve(mdp)

        return improved
