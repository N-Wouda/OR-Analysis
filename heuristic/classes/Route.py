from typing import List, Set, Tuple

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

    def can_insert(self, customer: int, at: int, problem: Problem) -> bool:
        """
        Checks if inserting a customer into this route at the given index at is
        feasible, that is, there is sufficient stack capacity to store the
        delivery and pickup items for the appropriate legs of the tour.

        O(n), where n is the number of customers in the route.
        """
        d_volume = problem.demands[customer]
        p_volume = problem.pickups[customer]
        max_capacity = problem.stack_capacity

        can_pickup = all(stacks.shortest_stack().volume() + p_volume <=
                         max_capacity for stacks in self.plan[at + 1:])

        can_deliver = all(stacks.shortest_stack().volume() + d_volume <=
                          max_capacity for stacks in self.plan[:at + 1])

        return can_pickup and can_deliver

    def opt_insert(self, customer: int, problem: Problem) -> Tuple[int, float]:
        """
        Optimal location and cost to insert customer into this route. Assumes it
        is feasible to do so.
        """
        costs = [self._insert_cost(customer, at, problem)
                 for at in range(len(self.customers) + 1)]

        opt_idx = np.argmin(costs).item()
        opt_cost = costs[opt_idx]

        return opt_idx, opt_cost

    def insert_customer(self, customer: int, at: int, problem: Problem):
        """
        Inserts customer in route at index at. Inserts customer delivery and
        pickup items into the appropriate parts of the loading plan. Assumes it
        is feasible to do so.
        """
        delivery = Item(problem.demands[customer], DEPOT, customer)
        pickup = Item(problem.pickups[customer], customer, DEPOT)

        self.customers.insert(at, customer)
        self._set.add(customer)

        # Makes a new loading plan for the just-inserted customer. This
        # initially looks like the loading plan for the previous customer.
        stack_after_customer = self.plan[at].copy()
        self.plan.insert(at + 1, stack_after_customer)

        # Inserts customer delivery item into the loading plan.
        for plan in self.plan[:at + 1]:
            plan.shortest_stack().push_rear(delivery)

        # Inserts customer pickup item into the loading plan.
        for plan in self.plan[at + 1:]:
            plan.shortest_stack().push_rear(pickup)

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

    def _insert_cost(self, customer: int, at: int, problem: Problem) -> float:
        """
        Computes cost of inserting customer in route at position at.
        """
        if at == 0:
            route = [DEPOT, customer, self.customers[0]]
        elif at == len(self.customers):
            route = [self.customers[-1], customer, DEPOT]
        else:
            route = [self.customers[at - 1], customer, self.customers[at]]

        route = np.array(route) + 1

        return problem.distances[route[0], route[1]] \
               + problem.distances[route[1], route[2]]
