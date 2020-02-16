from __future__ import annotations

from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from alns import State

from heuristic.constants import DEPOT, TEAM_NUMBER
from .Problem import Problem
from .Route import Route


class Solution(State):
    problem: Problem
    routes: List[Route]

    unassigned: List[int]

    def copy(self) -> Solution:
        """
        Returns a copy of the current Solution object.
        """
        solution = Solution()
        solution.problem = self.problem
        solution.routes = deepcopy(self.routes)

        return solution

    @classmethod
    def empty(cls, problem: Problem) -> Solution:
        """
        Creates an empty Solution object, with the passed-in Problem instance.
        """
        solution = cls()
        solution.problem = problem
        solution.routes = []

        return solution

    def objective(self) -> float:
        """
        Evaluates the current solution.
        """
        return sum(route.cost(self.problem) for route in self.routes)

    def plot(self):
        """
        Plots the current solution state.
        """
        # TODO
        plt.draw_if_interactive()

    @classmethod
    def from_file(cls, location: str) -> Solution:
        pass

    def to_file(self, location: str):
        with open(location, 'w+') as file:
            print(TEAM_NUMBER, file=file)
            print(self.problem.instance, file=file)
            print(len(self.routes), file=file)

            for idx_route, route in enumerate(self.routes, 1):
                legs = np.array([DEPOT, *route.customers])
                legs += 1

                for idx_leg, leg in enumerate(legs):
                    stacks = route.plan.snapshots[idx_leg]

                    for idx_stack, stack in enumerate(stacks, 1):
                        print(f"V{idx_route},{leg},S{idx_stack},{stack}",
                              file=file)
