from typing import List, Set

import numpy as np

from heuristic.constants import DEPOT
from .Problem import Problem
from .Stacks import Stacks
from .Item import Item


class Route:
    customers: List[int]  # customers visited, in order (indices)
    _customers: Set[int]  # for customer membership checks
    plan: List[Stacks]  # loading plan

    def __init__(self, customers: List[int], plan: List[Stacks]):
        self.customers = customers
        self._customers = set(customers)
        self.plan = plan

    def __contains__(self, customer: int) -> bool:
        return customer in self._customers

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
        about O(|customers| * num_stacks * n), where n is the number of items
        in a stack.
        """
        assert len(self.customers) + 1 == len(self.plan)

        cost = 0.

        for idx, customer in enumerate(self.customers):
            # Stack lay-outs before and after the current customer.
            before, after = self.plan[idx:idx + 2]
            cost += Stacks.cost(customer, problem, before, after)

        return cost

    def remove_customer(self, customer: int, problem: Problem):
        """
        Removes the passed-in customer from this route, and updates the
        loading plan to reflect this change. O(n * m), where n is the number
        of customers, and m the length of the longest stack (in number of
        items).

        TODO this must be done faster.
        """
        delivery = Item(problem.demands[customer], DEPOT, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        idx = self.customers.index(customer)

        # Removes customer delivery item from the loading plan.
        for stacks in self.plan[:idx]:
            stack = stacks.find_stack(delivery)
            stack.remove(delivery)

        # Removes customer pickup item from the loading plan.
        for stacks in self.plan[(idx + 1):]:
            stack = stacks.find_stack(pickup)
            stack.remove(pickup)

        # And finally, removes the customer itself.
        del self.customers[idx]
        del self.plan[idx]
        self._customers.remove(customer)
