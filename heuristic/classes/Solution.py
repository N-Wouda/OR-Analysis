from __future__ import annotations

from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from alns import State

from heuristic.constants import DEPOT, TEAM_NUMBER
from .Problem import Problem
from .Route import Route
from .Stack import Stack
from .Stacks import Stacks


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
        solution.unassigned = deepcopy(self.unassigned)

        return solution

    @classmethod
    def empty(cls, problem: Problem) -> Solution:
        """
        Creates an empty Solution object, with the passed-in Problem instance.
        """
        solution = cls()
        solution.problem = problem
        solution.routes = []
        solution.unassigned = []

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
        n_rows = len(self.routes)
        n_cols = max(len(route.customers) + 1 for route in self.routes)

        _, axes = plt.subplots(n_rows, n_cols, figsize=(2.5 * n_cols, n_rows))

        for row, route in enumerate(self.routes):
            axes[row, 0].set_ylabel(f"Route {row + 1}")

            for col, stacks in enumerate(route.plan):
                ax = axes[row, col]

                ax.barh(np.arange(self.problem.num_stacks),
                        [stack.volume() for stack in stacks])

                ax.set_xlim(right=self.problem.stack_capacity)
                ax.set_yticks(np.arange(self.problem.num_stacks))
                ax.margins(x=0, y=0)

                ax.set_xlabel(f"DEPOT" if col == 0 else
                              f"CUST {route.customers[col - 1] + 1}")

                for idx in range(self.problem.num_stacks):
                    ax.text(self.problem.stack_capacity / 2,
                            idx,
                            str(stacks[idx]),
                            ha='center',
                            va='center',
                            color='darkgrey')

        plt.show()

    @classmethod
    def from_file(cls, problem: Problem, location: str) -> Solution:
        """
        Reads a solution to the passed-in problem from the file system.
        """
        solution = cls.empty(problem)

        with open(location) as file:
            data = file.readlines()

            solution.routes = [Route([], []) for _ in range(int(data[2]))]

            data = data[3:]  # first three lines are metadata

        for line in data:
            vehicle, node, stack, *items = line.strip().split(",")

            idx_route = int(vehicle[1]) - 1
            assert idx_route >= 0

            route = solution.routes[idx_route]

            idx_stack = int(stack[1]) - 1
            assert idx_stack >= 0

            if idx_stack == 0:
                route.plan.append(Stacks(problem.num_stacks))

            customer = int(node) - 1

            if customer != DEPOT:
                route.customers.append(customer)

            route.plan[-1].stacks[idx_stack] = Stack.from_strings(items,
                                                                  problem)

        return solution

    def to_file(self, location: str):
        """
        Writes this solution to the file system.
        """
        file = open(location, 'w+')

        print(TEAM_NUMBER, file=file)
        print(self.problem.instance, file=file)
        print(len(self.routes), file=file)

        for idx_route, route in enumerate(self.routes, 1):
            legs = np.array([DEPOT, *route.customers])
            legs += 1

            for idx_leg, leg in enumerate(legs):
                for idx_stack, stack in enumerate(route.plan[idx_leg], 1):
                    print(f"V{idx_route},{leg},S{idx_stack},{stack}", file=file)

        file.close()
