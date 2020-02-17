from typing import List

import numpy as np

from heuristic.constants import DEPOT
from .Problem import Problem
from .Stacks import Stacks
from .Item import Item


class Route:
    customers: List[int]  # customers visited, in order (indices)
    plan: List[Stacks]  # loading plan

    def __init__(self, customers: List[int], plan: List[Stacks]):
        self.customers = customers
        self.plan = plan

    def cost(self, problem: Problem) -> float:
        """
        Computes the cost (objective) value of this route, based on the
        distance and handling costs.
        """
        return self._route_cost(problem) + self._plan_cost(problem)

    def _route_cost(self, problem: Problem) -> float:
        """
        Determines the route cost connecting the passed-in customers. Assumes
        the DEPOT is excluded in the customers list; it will be added here.
        O(|customers|).
        """
        customers = np.array([DEPOT, *self.customers, DEPOT])
        customers += 1

        return sum(problem.distances[first, second]
                   for first, second in zip(customers, customers[1:]))

    def _plan_cost(self, problem: Problem) -> float:
        """
        Computes the handling cost of the current loading plan. This is done
        by determining the cost of the mutations at each customer. Runs in
        about O(|customers| * |num_stacks| * n), where n is the number of items
        in a stack.
        """
        assert len(self.customers) + 1 == len(self.plan)

        cost = 0.

        for idx, customer in enumerate(self.customers):
            # Stack lay-outs before and after the current customer.
            before, after = self.plan[idx:idx + 2]
            cost += Stacks.cost(customer, problem, before, after)

        return cost

    def remove_customer(self, customer: int):
        """
        Removes customer from route and items with the customer as destination
        or origin from the loading plan.
        """
        idx = self.customers.index(customer)
        delivery_item = Item(Problem.demands[customer], DEPOT, customer)
        pickup_item = Item(Problem.demands[customer], customer, DEPOT)

        for stacks in self.plan[:(idx - 1)]:
            stack = stacks.find_stack(delivery_item)
            stack.stack.remove(delivery_item)

        for stacks in self.plan[idx:]:
            stack = stacks.find_stack(pickup_item)
            stack.stack.remove(pickup_item)

        self.customers.remove(customer)
