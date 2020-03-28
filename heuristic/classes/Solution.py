from __future__ import annotations

from copy import copy, deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from alns import State

from heuristic.constants import DEPOT, TEAM_NUMBER
from .Problem import Problem
from .Route import Route
from .Stacks import Stacks


class Solution(State):
    __slots__ = ['routes', 'unassigned']

    routes: List[Route]
    unassigned: List[int]

    def __init__(self, routes: List[Route], unassigned: List[int]):
        self.routes = routes
        self.unassigned = unassigned

    def __copy__(self):
        return Solution(copy(self.routes), copy(self.unassigned))

    def __deepcopy__(self, memodict={}):
        return Solution(deepcopy(self.routes), deepcopy(self.unassigned))

    def find_route(self, customer: int) -> Route:
        """
        Finds and returns the Route containing the passed-in customer. Raises
        a LookupError if no such Route exists. O(num_routes).
        """
        for route in self.routes:
            if customer in route:
                return route

        raise LookupError(f"Customer {customer} is not understood.")

    def cost(self) -> float:
        """
        Wrapper to play nice with the local search procedure. Returns the
        objective value for this solution instance.
        """
        return self.objective()

    def objective(self) -> float:
        """
        Evaluates the current solution.
        """
        return sum(route.cost() for route in self.routes)

    def plot(self):
        """
        Plots the current solution state.
        """
        # Number of columns is customers + depot, and a final column for route
        # cost.
        n_cols = max(len(route) for route in self.routes) + 2
        n_rows = len(self.routes)

        _, axes = plt.subplots(n_rows, n_cols, figsize=(2.5 * n_cols, n_rows),
                               squeeze=False)

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

            last = len(route.plan)

            # Hide empty route cells (these are used by some routes, but not
            # all).
            for col in range(last, n_cols):
                axes[row, col].set_axis_off()

            # These lines display some route statistics (routing and handling
            # costs). Default size is [0, 1] x [0, 1] - these numbers place the
            # text nicely centered.
            axes[row, last].text(0, .6, f"[RC] {route.routing_cost():.2f}")
            axes[row, last].text(0, .2, f"[HC] {route.handling_cost():.2f}")

        plt.show()

    @classmethod
    def from_file(cls, location: str) -> Solution:
        """
        Reads a solution from the file system.
        """
        problem = Problem()

        with open(location) as file:
            data = file.readlines()

        routes = [Route([], []) for _ in range(int(data[2]))]
        data = data[3:]  # first three lines are metadata

        for line in data:
            vehicle, node, stack, *items = line.strip().split(",")

            idx_route = int(vehicle[1:]) - 1
            route = routes[idx_route]

            customer = int(node) - 1

            if customer != DEPOT and customer not in route:
                route.customers.append(customer)

            idx_stack = int(stack[1:]) - 1

            if idx_stack == 0:  # new loading plan (next leg).
                route.plan.append(Stacks(problem.num_stacks))

            stack = route.plan[-1][idx_stack]

            for str_item in items:
                if not str_item:  # empty stack
                    continue

                item_type = str_item[0]
                customer = int(str_item[1:]) - 1

                if item_type == "d":
                    stack.push_rear(problem.demands[customer])
                else:
                    stack.push_rear(problem.pickups[customer])

        return Solution(routes, [])

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
