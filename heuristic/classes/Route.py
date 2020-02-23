from typing import List, Optional, Set, Tuple

from collections import deque
import numpy as np
from copy import deepcopy

from heuristic.constants import DEPOT
from .Problem import Problem
from .Stacks import Stacks


class Route:
    customers: List[int]  # customers visited, in order (indices)
    _set: Set[int]
    plan: List[Stacks]  # loading plan

    _route_cost: Optional[float] = None
    _handling_cost: Optional[float] = None

    def __init__(self, customers: List[int], plan: List[Stacks]):
        self.customers = customers
        self._set = set(customers)
        self.plan = plan

    def __contains__(self, customer: int) -> bool:
        return customer in self._set

    def cost(self) -> float:
        """
        Returns the cost (objective) value of this route, based on the
        distance and handling costs.
        """
        return self.routing_cost() + self.handling_cost()

    def routing_cost(self) -> float:
        """
        Determines the route cost connecting this route's customers, and the
        DEPOT. O(1).
        """
        if self._route_cost is None:
            self._route_cost = self._compute_routing_cost()

        return self._route_cost

    def handling_cost(self) -> float:
        """
        Determines the handling cost for this route. O(1).
        """
        if self._handling_cost is None:
            self._handling_cost = self._compute_handling_cost()

        return self._handling_cost

    def can_insert(self, customer: int, at: int) -> bool:
        """
        Checks if inserting a customer into this route at the given index at is
        feasible, that is, there is sufficient stack capacity to store the
        delivery and pickup items for the appropriate legs of the tour.

        O(n), where n is the number of customers in the route.
        """
        problem = Problem()

        d_item = problem.demands[customer]
        p_item = problem.pickups[customer]
        max_capacity = problem.stack_capacity

        can_pickup = all(stacks.shortest_stack().volume() + d_item.volume
                         <= max_capacity for stacks in self.plan[at + 1:])

        can_deliver = all(stacks.shortest_stack().volume() + p_item.volume
                          <= max_capacity for stacks in self.plan[:at + 1])

        return can_pickup and can_deliver

    def opt_insert(self, customer: int) -> Tuple[int, float]:
        """
        Optimal location and cost to insert customer into this route. Assumes it
        is feasible to do so.
        """
        costs = [self._insert_cost(customer, at)
                 for at in range(len(self.customers) + 1)]

        opt_idx = np.argmin(costs).item()
        opt_cost = costs[opt_idx]

        return opt_idx, opt_cost

    def insert_customer(self, customer: int, at: int):
        """
        Inserts customer in route at index at. Inserts customer delivery and
        pickup items into the appropriate parts of the loading plan. Assumes it
        is feasible to do so.
        """
        problem = Problem()

        self.customers.insert(at, customer)
        self._set.add(customer)

        # Makes a new loading plan for the just-inserted customer. This
        # initially looks like the loading plan for the previous customer.
        stack_after_customer = self.plan[at].copy()
        self.plan.insert(at + 1, stack_after_customer)

        # Inserts customer delivery item into the loading plan.
        for plan in self.plan[:at + 1]:
            plan.shortest_stack().push_rear(problem.demands[customer])

        # Inserts customer pickup item into the loading plan.
        for plan in self.plan[at + 1:]:
            plan.shortest_stack().push_rear(problem.pickups[customer])

        self._invalidate_cached_costs()

    def remove_customer(self, customer: int):
        """
        Removes the passed-in customer from this route, and updates the
        loading plan to reflect this change. O(n * m), where n is the tour
        length, and m the length of the longest stack (in number of items).
        """
        problem = Problem()

        delivery = problem.demands[customer]
        pickup = problem.pickups[customer]

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

        self._invalidate_cached_costs()

    def _insert_cost(self, customer: int, at: int) -> float:
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
        problem = Problem()

        return problem.distances[route[0], route[1]] \
               + problem.distances[route[1], route[2]]

    def sort_depot_deliveries(self):
        """
        Sorts the stacks at the depot such that the deliveries are sorted in
        the reverse order in which the customers are visited.
        """
        for stack in self.plan[0]:
            order = self.customers
            stack.stack = deque(sorted(stack.stack,
                                       key=lambda item: order.index(
                                           item.destination)))

    def sort_customer_quantities(self):
        """
        Sorts stacks by the following policy: if the cost of moving the pickup
        at every customer after the current one is smaller than the cost of
        placing it in the front of the stack at the current customer, it is
        placed in the rear; otherwise it is placed in the front.
        """
        problem = Problem()
        for idx in range(1, len(self.plan)):

            self.plan[idx] = self.plan[idx - 1].copy()

            customer = self.customers[idx - 1]
            delivery = problem.demands[customer]
            stack = self.plan[idx].find_stack(delivery)
            stack.remove(delivery)

            volume_rest = sum(
                problem.pickups[it].volume for it in
                range(idx + 1, len(self.plan)))

            if problem.pickups[customer].volume * len(
                    self.customers[idx:]) >= volume_rest:
                self.plan[idx].shortest_stack().push_rear(
                    problem.pickups[customer])
            else:
                self.plan[idx].shortest_stack().push_effective_front(
                    problem.pickups[customer])

    def _compute_routing_cost(self) -> float:
        """
        Determines the route cost connecting the passed-in customers. Assumes
        the DEPOT is excluded in the customers list; it will be added here.
        O(|customers|).
        """
        customers = np.array(self.customers + [DEPOT])
        customers += 1

        # See e.g. https://stackoverflow.com/a/53276900/4316405
        return Problem().distances[np.roll(customers, 1), customers].sum()

    def _compute_handling_cost(self) -> float:
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
            cost += Stacks.cost(customer, before, after)

        return cost

    def _invalidate_cached_costs(self):
        """
        Resets the cached handling and routing costs.
        """
        self._handling_cost = None
        self._route_cost = None
