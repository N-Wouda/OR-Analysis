from typing import List, Optional, Set, Tuple

import numpy as np

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

        self._route_cost = Route.distance([DEPOT] + customers + [DEPOT])

    def __contains__(self, customer: int) -> bool:
        return customer in self._set

    def cost(self) -> float:
        """
        Returns the cost (objective) value of this route, based on the
        distance and handling costs.
        """
        return self.routing_cost() + self.handling_cost()

    @staticmethod
    def distance(customers: List[int]) -> float:
        """
        Computes the distance for the passed-in list of visited customer nodes.
        Does not assume this list forms a tour. O(|customers|).
        """
        problem = Problem()
        customers = np.array(customers) + 1

        return sum(problem.distances[first, second]
                   for first, second in zip(customers, customers[1:]))

    def routing_cost(self) -> float:
        """
        Determines the route cost connecting this route's customers, and the
        DEPOT. O(1).
        """
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

        d_volume = problem.demands[customer].volume
        p_volume = problem.pickups[customer].volume
        max_capacity = problem.stack_capacity

        # Similarly, we insert the customer pick-up item into the shortest
        # stack at the customer. This should be feasible for all appropriate
        # legs of the tour.
        shortest_customer = self.plan[at].shortest_stack()
        can_pickup = all(stacks[shortest_customer.index].volume() + d_volume
                         <= max_capacity for stacks in self.plan[at + 1:])

        # We insert the customer's delivery item into the shortest stack at the
        # depot. This should be feasible for all appropriate legs of the tour.
        shortest_depot = self.plan[0].shortest_stack()
        can_deliver = all(stacks[shortest_depot.index].volume() + p_volume
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
        # TODO policy? We currently always push onto the rear.
        problem = Problem()

        self.customers.insert(at, customer)
        self._set.add(customer)

        # Makes a new loading plan for the just-inserted customer, by copying
        # the previous customer's loading plan and inserting customer items.
        self.plan.insert(at + 1, self.plan[at].copy())

        # Inserts customer delivery item into the loading plan. The stack to
        # insert into is the shortest stack at the depot (since the delivery
        # item is carried from the depot to the customer).
        stack_idx = self.plan[0].shortest_stack().index

        for plan in self.plan[:at + 1]:
            plan.stacks[stack_idx].push_rear(problem.demands[customer])

        # Inserts customer pickup item into the loading plan. The stack to
        # insert into is the shortest stack at the customer (since the pickup
        # item is carried from the customer to the depot).
        stack_idx = self.plan[at + 1].shortest_stack().index

        for plan in self.plan[at + 1:]:
            plan.stacks[stack_idx].push_rear(problem.pickups[customer])

        # Updates routing costs. Handling costs are more complicated, and best
        # recomputed entirely.
        self._update_routing_cost(customer, at, "insert")
        self._handling_cost = None

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

        # Updates routing costs. Handling costs are more complicated, and best
        # recomputed entirely.
        self._update_routing_cost(customer, idx, "remove")
        self._handling_cost = None

    def _insert_cost(self, customer: int, at: int) -> float:
        """
        Computes the routing cost of inserting customer in route at position
        at.

        Note: NW attempted this with relative improvements of 1 -> 2 -> 3
        minus 1 -> 3 (if we're inserting 2), but that did not improve costs.
        Perhaps that's too restrictive?
        """
        if at == 0:
            return Route.distance([DEPOT, customer, self.customers[0]])

        if at == len(self.customers):
            return Route.distance([self.customers[-1], customer, DEPOT])

        return Route.distance([self.customers[at - 1],
                               customer,
                               self.customers[at]])

    def _update_routing_cost(self, customer: int, idx: int, update_type):
        """
        Updates the routing cost for this Route, which is a cached property.
        For removals, it removes the cost of [from] -> [cust] -> [next], and
        adds the cost of [from] -> [next]. For insertions, it does the
        opposite.

        Raises
        ------
        ValueError
            When the update type is not understood.
        """
        prev_leg = DEPOT if idx == 0 else self.customers[idx - 1]

        # For a removal, the next customer is now at the customer's index. For
        # an insert, it's one further.
        if update_type == "insert":
            idx += 1

        next_leg = DEPOT if idx == len(self.customers) else self.customers[idx]

        if update_type == "remove":
            self._route_cost -= Route.distance([prev_leg, customer, next_leg])
            self._route_cost += Route.distance([prev_leg, next_leg])
        elif update_type == "insert":
            self._route_cost += Route.distance([prev_leg, customer, next_leg])
            self._route_cost -= Route.distance([prev_leg, next_leg])
        else:
            raise ValueError(f"Update type `{update_type}' is not understood.")

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

    def __str__(self):
        return str(np.array([DEPOT] + self.customers + [DEPOT]) + 1)

    def __repr__(self):
        return f"Route({str(self)}"
