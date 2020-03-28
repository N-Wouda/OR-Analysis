import operator
from copy import deepcopy
from itertools import islice, takewhile, tee
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from heuristic.constants import DEPOT
from .Item import Item
from .Problem import Problem
from .SetList import SetList
from .Stacks import Stacks


class Route:
    __slots__ = ['customers', 'plan', '_route_cost', '_handling_cost']

    customers: SetList[int]  # visited customers
    plan: List[Stacks]  # loading plan

    _route_cost: Optional[float]  # cached results
    _handling_cost: Optional[float]

    def __init__(self,
                 customers: Union[List[int], SetList[int]],
                 plan: List[Stacks]):
        self.customers = SetList(customers)
        self.plan = plan

        self._route_cost = None
        self._handling_cost = None

    def __contains__(self, customer: int) -> bool:
        return customer in self.customers

    def __len__(self):
        return len(self.customers)

    def __iter__(self):
        yield from self.customers

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

        # Constructs two iterators from the passed-in customers. This is fairly
        # efficient, as it avoids copying.
        from_custs, to_custs = tee(customers)
        next(to_custs, None)

        return sum(problem.distances[first + 1, second + 1]
                   for first, second in zip(from_custs, to_custs))

    @property
    def indices(self) -> Dict[int, int]:
        return {customer: idx for idx, customer in enumerate(self.customers)}

    def attempt_append_tail(self, customers: List[int]) -> bool:
        """
        This method attempts to append the passed-in customers to this route.
        It might fail if the capacity constraints cannot be respected (returns
        False) - if it succeeds, the route is updated with the new customers
        and True is returned.

        The invariant is thus: if the method succeeds, this route has appended
        the passed-in customers. If the method fails, the route remains
        unchanged.
        """
        for idx, customer in enumerate(customers):
            if self.can_insert(customer, len(self)):
                self.insert_customer(customer, len(self))
            else:
                for customer in customers[:idx]:
                    self.remove_customer(customer)

                return False

        return True

    def invalidate_routing_cache(self):
        self._route_cost = None

    def invalidate_handling_cache(self):
        self._handling_cost = None

    def routing_cost(self) -> float:
        """
        Determines the route cost connecting this route's customers, and the
        DEPOT. O(1).
        """
        if self._route_cost is None:
            route = [DEPOT] + self.customers.to_list() + [DEPOT]
            self._route_cost = Route.distance(route)

        return self._route_cost

    def handling_cost(self) -> float:
        """
        Determines the handling cost for this route. O(1), generally.
        """
        if self._handling_cost is None:
            assert len(self.customers) + 1 == len(self.plan)

            self._handling_cost = 0.

            for idx, customer in enumerate(self.customers):
                before, after = self.plan[idx], self.plan[idx + 1]
                self._handling_cost += Stacks.cost(customer, before, after)

        return self._handling_cost

    def can_insert(self, customer: int, at: int) -> bool:
        """
        Checks if inserting a customer into this route at the given index at is
        feasible, that is, there is sufficient stack capacity to store the
        delivery and pickup items for the appropriate legs of the tour.

        O(n), where n is the number of customers in the route.
        """
        problem = Problem()

        # We insert the customer's delivery item into the shortest stack at the
        # depot. Including at: we need to make sure the delivery item  fits into
        # stacks up to and including the customer before at, and the depot.
        can_deliver = self.can_insert_item(problem.demands[customer],
                                           self.plan[0].shortest_stack().index,
                                           at + 1)

        if not can_deliver:
            # This is already infeasible, and cutting it off here saves another
            # computation below.
            return False

        # Similarly, we insert the customer pick-up item into the shortest stack
        # at the customer. From at, since we copy at and turn it into the
        # customer's loading plan (which should be feasible).
        can_pickup = self.can_insert_item(problem.pickups[customer],
                                          self.plan[at].shortest_stack().index,
                                          at)

        return can_deliver and can_pickup

    def can_insert_item(self,
                        item: Item,
                        stack_idx: int,
                        customer_at: Optional[int] = None) -> bool:
        """
        Tests if the given item can be inserted into the stack indicated by
        stack_idx for all appropriate legs of the tour, up to customer_at (for
        a delivery item), or from customer_at (for a pickup item).

        If customer_at is not passed, it is assumed the customer is in this
        route.
        """
        if customer_at is None:
            customer_at = self.customers.index(item.customer)

        problem = Problem()

        if item.is_delivery():
            plans = self.plan[:customer_at]
        else:
            plans = self.plan[customer_at:]

        return all(plan[stack_idx].volume() + item.volume
                   <= problem.stack_capacity for plan in plans)

    def opt_insert(self, customer: int) -> Tuple[int, float]:
        """
        Optimal feasible location and cost to insert customer into this route.
        Assumes it is feasible to do so.
        """
        costs = [self._insert_cost(customer, at)
                 for at in range(len(self.customers) + 1)]

        # noinspection PyTypeChecker
        return min(enumerate(costs), key=operator.itemgetter(1))

    def insert_customer(self, customer: int, at: int):
        """
        Inserts customer in route at index at. Inserts customer delivery and
        pickup items into the appropriate parts of the loading plan. Assumes it
        is feasible to do so.
        """
        problem = Problem()

        self.customers.insert(at, customer)
        self.plan.insert(at + 1, deepcopy(self.plan[at]))

        # Inserts customer delivery item into the loading plan. The stack to
        # insert into is the shortest stack at the depot (since the delivery
        # item is carried from the depot to the customer).
        stack_idx = self.plan[0].shortest_stack().index
        delivery = problem.demands[customer]

        for plan in self.plan[:at + 1]:
            plan[stack_idx].push_rear(delivery)

        pickup = problem.pickups[customer]
        stack = self.plan[at + 1].shortest_stack()

        # Pickups in the front (these are never moved, so we might want to
        # insert our pick-up item just after them, nearer to the rear).
        front = list(takewhile(lambda item: item.is_pickup(), reversed(stack)))

        # The pickup item will have to be moved for each delivery item that's
        # currently in the stack, if we insert it in the rear.
        volume = stack.deliveries_in_stack() * pickup.volume

        # Tests if placing the pick-up item near the front is cheaper than
        # inserting it in the rear. The former incurs costs *now*, whereas for
        # the latter the item might have to move at later points in the tour.
        if stack.volume() - sum(item.volume for item in front) < volume:
            # It is also best to move any pickup items that are not already
            # near the front, as those are to be moved now anyway.
            pickups = [item for item in islice(stack, len(stack) - len(front))
                       if item.is_pickup()]

            for plan in self.plan[at + 1:]:
                for item in pickups:
                    plan[stack.index].remove(item)
                    plan[stack.index].push(-len(front), item)

                plan[stack.index].push(-len(front), pickup)
        else:
            for plan in self.plan[at + 1:]:
                plan[stack.index].push_rear(pickup)

        self._update_routing_cost(customer, at, "insert")
        self.invalidate_handling_cache()

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

        self._update_routing_cost(customer, idx, "remove")
        self.invalidate_handling_cache()

        for stacks in self.plan[:idx + 1]:
            stacks.find_stack(delivery).remove(delivery)

        for stacks in self.plan[idx + 1:]:
            stacks.find_stack(pickup).remove(pickup)

        del self.customers[idx]
        del self.plan[idx + 1]

    def _insert_cost(self, customer: int, at: int) -> float:
        """
        Computes the routing cost of inserting customer in route at position
        at.

        Note: NW attempted this with relative improvements of 1 -> 2 -> 3
        minus 1 -> 3 (if we're inserting 2), but that did not improve costs.
        Perhaps that's too restrictive?
        """
        problem = Problem()

        if at == 0:
            return problem.short_distances[DEPOT, customer, self.customers[0]]

        if at == len(self.customers):
            return problem.short_distances[self.customers[-1], customer, DEPOT]

        return problem.short_distances[self.customers[at - 1],
                                       customer,
                                       self.customers[at]]

    def _update_routing_cost(self, customer: int, idx: int, update_type):
        """
        Updates the routing cost for this Route, which is a cached property.
        For removals, it removes the cost of [from] -> [cust] -> [next], and
        adds the cost of [from] -> [next]. For insertions, it does the opposite.
        Called only when the customer is at or still at this index (so after
        insertion, and before removal).

        Raises
        ------
        ValueError
            When the update type is not understood.
        """
        if self._route_cost is None:  # computation can be delayed.
            return

        prev_leg = DEPOT if idx == 0 else self.customers[idx - 1]
        next_leg = DEPOT if idx == len(self.customers) - 1 \
            else self.customers[idx + 1]

        problem = Problem()

        if update_type == "remove":
            self._route_cost -= problem.short_distances[prev_leg,
                                                        customer,
                                                        next_leg]
            self._route_cost += problem.distances[prev_leg + 1, next_leg + 1]
        elif update_type == "insert":
            self._route_cost += problem.short_distances[prev_leg,
                                                        customer,
                                                        next_leg]
            self._route_cost -= problem.distances[prev_leg + 1, next_leg + 1]
        else:
            raise ValueError(f"Update type `{update_type}' is not understood.")

    def __str__(self):
        customers = np.array([DEPOT] + self.customers.to_list() + [DEPOT])
        customers += 1

        return f"{customers}, {self.plan}"

    def __repr__(self):
        return f"Route({self})"
