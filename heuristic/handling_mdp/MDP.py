import itertools
from functools import lru_cache
from typing import Dict, List, Tuple

from heuristic.classes import Problem, Route, Stack, Stacks
from heuristic.constants import DEPOT, NUM_BLOCKS
from .Block import Block

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
        return Stacks.cost(customer,
                           self.state_to_stacks(from_state, customer, False),
                           self.state_to_stacks(to_state, customer, True))

    def state_to_stacks(self,
                        state: State,
                        customer: int,
                        after: bool) -> Stacks:
        """
        Reconstructs a lay-out plan from the given state, just before or after
        the passed-in customer. O(|customers|), for the customers on the route.
        """
        problem = Problem()
        stacks = Stacks(problem.num_stacks)

        for idx in range(problem.num_stacks):
            start = idx * NUM_BLOCKS // problem.num_stacks
            end = start + NUM_BLOCKS // problem.num_stacks

            # Populates the stack at idx with the customer data in the assigned
            # blocks from state.
            self._populate_stack(stacks[idx], customer, state[start:end], after)

        return stacks

    def _populate_stack(self,
                        stack: Stack,
                        customer: int,
                        blocks: Tuple[Block],
                        after: bool):
        problem = Problem()
        cust_idx = self.indices[customer]

        for block_customer in itertools.chain.from_iterable(blocks):
            if self.indices[block_customer] == cust_idx and after \
                    or self.indices[block_customer] < cust_idx:
                # All customers visited along the route before this customer
                # are now pick-up items. This customer's item is a pick-up item
                # only if after is True, else it's a demand item.
                stack.push_rear(problem.pickups[block_customer])
            else:
                stack.push_rear(problem.demands[block_customer])
