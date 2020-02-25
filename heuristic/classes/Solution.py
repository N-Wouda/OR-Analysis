from __future__ import annotations

import pickle
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
    routes: List[Route]
    unassigned: List[int]

    def copy(self) -> Solution:
        """
        Returns a copy of the current Solution object.
        """
        return pickle.loads(pickle.dumps(self))

    @classmethod
    def empty(cls) -> Solution:
        """
        Creates an empty Solution object, with the passed-in Problem instance.
        """
        solution = cls()
        solution.routes = []
        solution.unassigned = []

        return solution

    def find_route(self, customer: int) -> Route:
        """
        Finds and returns the Route containing the passed-in customer. Raises
        a LookupError if no such Route exists. O(num_routes).
        """
        for route in self.routes:
            if customer in route:
                return route

        raise LookupError(f"Customer {customer} is not understood.")

    def objective(self) -> float:
        """
        Evaluates the current solution.
        """
        return sum(route.cost() for route in self.routes)

    def plot(self):
        """
        Plots the current solution state.
        """
        n_rows = len(self.routes)  # number of columns is customers + depot
        n_cols = max(len(route.customers) for route in self.routes) + 1

        _, axes = plt.subplots(n_rows, n_cols, figsize=(2.5 * n_cols, n_rows))

        problem = Problem()

        for row, route in enumerate(self.routes):
            axes[row, 0].set_ylabel(f"Route {row + 1}")

            for col, stacks in enumerate(route.plan):
                ax = axes[row, col]

                ax.barh(np.arange(problem.num_stacks),
                        [stack.volume() for stack in stacks])

                ax.set_xlim(right=problem.stack_capacity)
                ax.set_yticks(np.arange(problem.num_stacks))
                ax.margins(x=0, y=0)

                ax.set_xlabel(f"DEPOT" if col == 0 else
                              f"CUST {route.customers[col - 1] + 1}")

                for idx in range(problem.num_stacks):
                    ax.text(problem.stack_capacity / 2,
                            idx,
                            str(stacks[idx]),
                            ha='center',
                            va='center',
                            color='darkgrey')

            # Hide empty route cells (these are used by some routes, but not
            # all).
            for col in range(len(route.plan), n_cols):
                axes[row, col].set_axis_off()

        plt.show()

    @classmethod
    def from_file(cls, location: str) -> Solution:
        """
        Reads a solution from the file system.

        TODO perhaps rewrite this.
        """
        solution = cls.empty()
        problem = Problem()

        with open(location) as file:
            data = file.readlines()

        routes = [([], []) for _ in range(int(data[2]))]
        data = data[3:]  # first three lines are metadata

        for line in data:
            vehicle, node, stack, *items = line.strip().split(",")

            idx_route = int(vehicle[1:]) - 1
            assert idx_route >= 0

            route = routes[idx_route]

            idx_stack = int(stack[1:]) - 1
            assert idx_stack >= 0

            if idx_stack == 0:
                route[1].append(Stacks(problem.num_stacks))

            customer = int(node) - 1

            # TODO this is slow - check if this works for larger instances.
            if customer != DEPOT and customer not in route[0]:
                route[0].append(customer)

            route[1][-1].stacks[idx_stack] = Stack.from_strings(items)

        solution.routes = [Route(*route) for route in routes]
        return solution

    def to_file(self, location: str):
        """
        Writes this solution to the file system.
        """
        file = open(location, 'w+')

        print(TEAM_NUMBER, file=file)
        print(Problem().instance, file=file)
        print(len(self.routes), file=file)

        for idx_route, route in enumerate(self.routes, 1):
            legs = np.array([DEPOT, *route.customers])
            legs += 1

            for idx_leg, leg in enumerate(legs):
                for idx_stack, stack in enumerate(route.plan[idx_leg], 1):
                    print(f"V{idx_route},{leg},S{idx_stack},{stack}", file=file)

        file.close()
