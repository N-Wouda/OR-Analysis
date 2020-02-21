from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution


class LocalSearch:

    def __init__(self):
        self.operators: List[Callable[..., Solution]] = []

    def add_operator(self, operator: Callable):
        self.operators.append(operator)

    def __call__(self, current: Solution, rnd_state: RandomState) -> Solution:
        def improve(solution):
            for operator in self.operators:
                new_solution = operator(solution, rnd_state)

                if new_solution.objective() < solution.objective():
                    solution = improve(new_solution)
                    break

            return solution

        return improve(current.copy())
