from typing import List, Set

import numpy as np

from heuristic.constants import DEPOT
from .Item import Item
from .Problem import Problem
from .Stacks import Stacks


class Route:
    customers: List[int]  # customers visited, in order (indices)
    _set: Set[int]
    plan: List[Stacks]  # loading plan

    def __init__(self, customers: List[int], plan: List[Stacks]):
        self.customers = customers
        self._set = set(customers)
        self.plan = plan

    def __contains__(self, customer: int) -> bool:
        return customer in self._set

    def cost(self, problem: Problem) -> float:
        """
        Computes the cost (objective) value of this route, based on the
        distance and handling costs.
        """
        return self.routing_cost(problem) + self.handling_cost(problem)

    def routing_cost(self, problem: Problem) -> float:
        """
        Determines the route cost connecting the passed-in customers. Assumes
        the DEPOT is excluded in the customers list; it will be added here.
        O(|customers|).
        """
        customers = np.array(self.customers + [DEPOT])
        customers += 1

        # See e.g. https://stackoverflow.com/a/53276900/4316405
        return problem.distances[np.roll(customers, 1), customers].sum()

    def handling_cost(self, problem: Problem) -> float:
        """
        Computes the handling cost of the current loading plan. This is done
        by determining the cost of the mutations at each customer. Runs in
        about O(|customers| * n), where n is the number of items in a stack.
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
        """
        delivery = Item(problem.demands[customer], DEPOT, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        idx = self.customers.index(customer)

        # Removes customer delivery item from the loading plan.
        for stacks in self.plan[:idx + 1]:
            stacks.find_stack(delivery).remove(delivery)

        # Removes customer pickup item from the loading plan.
        for stacks in self.plan[idx + 1:]:
            stacks.find_stack(pickup).remove(pickup)

        # Removes the customer and its loading plan.
        del self.customers[idx]
        self._set.remove(customer)
        del self.plan[idx + 1]
