from typing import Callable

from numpy.random import RandomState

from heuristic.classes import Solution


class LocalSearch:

    def __init__(self):
        self.operators = []

    def add_operator(self, operator: Callable):
        self.operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        return current  # TODO
