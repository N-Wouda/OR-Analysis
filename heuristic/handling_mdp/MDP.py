from __future__ import annotations

from functools import lru_cache
from itertools import chain, permutations, product
from typing import Dict, List, Tuple

import numpy as np

from heuristic.classes import Problem, Route, Stack, Stacks
from heuristic.constants import DEPOT, NUM_BLOCKS
from .Block import Block
from .split import split

State = Tuple[Block]  # type alias


class MDP:
    states: List[State]
    route: Route
    legs: List[int]

    def __init__(self, states: List[State], route: Route):
        self.states = states
        self.route = route
        self.legs = [DEPOT] + route.customers.to_list()

    @property
    @lru_cache(1)
    def indices(self) -> Dict[int, int]:
        """
        Returns the indices for the DEPOT and customers on the route.
        """
        return {customer: idx for idx, customer
                in enumerate(self.legs)}

    def cost(self, customer: int, from_state: State, to_state: State) -> float:
        """
        Determines the costs of going from from_state before the passed-in
        customer, to the to_state after the passed-in customer. This information
        is used to reconstruct the stack lay-outs and determine the handling
        cost.
        """
        before = self.state_to_stacks(from_state, customer, False)
        after = self.state_to_stacks(to_state, customer, True)

        if before.is_feasible() and after.is_feasible():
            return Stacks.cost(customer, before, after)

        # Not all block assignments are actually feasible - we attempt to
        # prevent this by selecting 'nice' enough blocks, but that does not
        # prevent this entirely.
        return np.inf

    @classmethod
    def from_route(cls, route: Route) -> MDP:
        """
        Constructs a simple MDP for the given route. This MDP consists of
        blocks, each containing some customers on the route. The MDP will solve
        the loading plan using these blocks to near-optimality.
        """
        if len(route.customers) <= NUM_BLOCKS:
            # This we can solve optimally, with a block for each customer.
            blocks = [Block([]) for _ in
                      range(NUM_BLOCKS - len(route.customers))]
            blocks.extend(Block([customer]) for customer in route.customers)
        else:
            # Create NUM_BLOCKS of customers by grouping nearby customers on the
            # route. These blocks are approximately balanced.
            blocks = list(map(Block, split(route.customers, NUM_BLOCKS)))

        assert len(blocks) == NUM_BLOCKS
        return cls(list(permutations(blocks)), route)

    def state_to_stacks(self,
                        state: State,
                        customer: int,
                        after: bool) -> Stacks:
        """
        Reconstructs a lay-out plan from the given state, just before or after
        the passed-in customer. O(|customers|), for the customers on the route.

        NB: Splitting based on https://stackoverflow.com/a/2135920/4316405.
        """
        problem = Problem()
        stacks = Stacks(problem.num_stacks)

        per_stack, remainder = divmod(len(state), problem.num_stacks)

        for idx in range(problem.num_stacks):
            blocks = state[idx * per_stack + min(idx, remainder)
                           :(idx + 1) * per_stack + min(idx + 1, remainder)]

            # Populates the stack at idx with the customer data in the assigned
            # blocks.
            self._populate_stack(stacks[idx], customer, blocks, after)

        return stacks

    def solve(self) -> List[Stacks]:
        """
        Determines an optimal loading plan in blocks for each leg of the MDP's
        route. O(|customers| * NUM_BLOCKS!), where customers are the customers
        in the MDP's route.
        """
        costs = np.empty((len(self.legs), len(self.states)))
        costs[-1, :] = 0.

        decisions = np.empty((len(self.legs) - 1, len(self.states)), dtype=int)
        leg_cost = np.empty((len(self.states), len(self.states)))

        for next_customer in range(len(self.legs) - 1, 0, -1):
            curr_customer = next_customer - 1

            for from_state, to_state in product(range(len(self.states)),
                                                repeat=2):
                next_cost = costs[next_customer, to_state]

                # Current cost is the cost made for leaving the current customer
                # with from_state, and leaving the next customer with to_state.
                curr_cost = self.cost(self.legs[next_customer],
                                      self.states[from_state],
                                      self.states[to_state])

                leg_cost[from_state, to_state] = curr_cost + next_cost

            costs[curr_customer, :] = np.min(leg_cost, axis=1)
            decisions[curr_customer, :] = np.argmin(leg_cost, axis=1)

        return self.plan(costs, decisions)

    def plan(self, costs: np.ndarray, decisions: np.ndarray) -> List[Stacks]:
        """
        Creates a loading plan from the passed-in optimal costs and decisions.
        This loading plan may then be used to update the route.
        """
        layouts = [np.argmin(costs[0, :])]

        for idx, _ in enumerate(self.route.customers):
            layouts.append(decisions[idx, layouts[-1]])

        # When idx == 0 we are at the depot, and we do not have anything to
        # unload (so the state consists of all demands in that case).
        return [self.state_to_stacks(self.states[layout],
                                     self.legs[idx],
                                     idx != 0)
                for idx, layout in enumerate(layouts)]

    def _populate_stack(self,
                        stack: Stack,
                        customer: int,
                        blocks: Tuple[Block],
                        after: bool):
        problem = Problem()
        cust_idx = self.indices[customer]

        for block_customer in chain.from_iterable(blocks):
            if self.indices[block_customer] == cust_idx and after \
                    or self.indices[block_customer] < cust_idx:
                # All customers visited along the route before this customer
                # are now pick-up items. This customer's item is a pick-up item
                # only if after is True, else it's a demand item.
                stack.push_rear(problem.pickups[block_customer])
            else:
                stack.push_rear(problem.demands[block_customer])
