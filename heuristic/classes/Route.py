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

    def is_feasible(self, problem: Problem, customer: int) -> bool:
        """
        Checks if inserting a customer in this route is feasible.
        """
        delivery = Item(problem.demands[customer], DEPOT, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        if all(stacks.shortest_stack().volume() + delivery.volume <=
               problem.stack_capacity for stacks in self.plan[:customer]) and \
                all(stacks.shortest_stack().volume() + pickup.volume <=
                    problem.stack_capacity for stacks in self.plan[customer:]):
            return True
        return False

    def insert_cost(self, problem: Problem, idx: int, customer: int) -> float:
        """
        Computes cost of inserting customer in route at idx.
        """
        full_route = np.array([DEPOT, *self.customers, DEPOT])
        full_route += 1

        idx += 1

        result = problem.distances[full_route[idx - 1], customer + 1] + \
                 problem.distances[customer + 1, full_route[idx]]

        return result

    def opt_insert(self, problem: Problem, customer: int) -> int:
        """
        Optimal location and cost to input customer in route, does not check
        feasibility.
        """
        full_route = np.array([DEPOT, *self.customers, DEPOT])
        full_route += 1

        insertion_costs = np.full(len(full_route) - 1, np.inf)

        for it, (first, second) in enumerate(zip(full_route, full_route[1:])):
            insertion_costs[it] = \
                problem.distances[first, customer + 1] \
                + problem.distances[customer + 1, second]

        return np.argmin(insertion_costs)

    def remove_customer(self, customer: int, problem: Problem):
        """
        Removes the passed-in customer from this route, and updates the
        loading plan to reflect this change. O(n * m), where n is the tour
        length, and m the length of the longest stack (in number of items).
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
