from functools import lru_cache
from typing import Dict, List, Tuple

from heuristic.classes import Problem, Route, Stack, Stacks
from heuristic.constants import DEPOT, NUM_BLOCKS_PER_STACK
from .Block import Block

State = Tuple[Block]  # type alias


class MDP:
    # TODO clean this whole thing.
    states: List[State]
    route: Route

    def __init__(self, states, route):
        self.states = states
        self.route = route
        self.customers = [DEPOT] + route.customers

    @property
    @lru_cache(1)
    def indices(self) -> Dict[int, int]:
        return {customer: idx for idx, customer
                in enumerate(self.customers)}

    def cost(self, customer: int, from_state: State, to_state: State) -> float:
        before = self.stacks_from_state(from_state, customer, False)
        after = self.stacks_from_state(to_state, customer, True)

        return Stacks.cost(customer, before, after)

    def stacks_from_state(self,
                          state: State,
                          customer: int,
                          is_pickup: bool) -> Stacks:
        problem = Problem()
        stacks = Stacks(problem.num_stacks)

        for idx in range(problem.num_stacks):
            start = idx * NUM_BLOCKS_PER_STACK
            end = start + NUM_BLOCKS_PER_STACK

            stacks[idx] = self._from_blocks(customer,
                                            idx,
                                            state[start:end],
                                            is_pickup)

        return stacks

    def _from_blocks(self, customer: int, idx: int, blocks, is_pickup) -> Stack:
        stack = Stack(idx)
        problem = Problem()

        to_idx = self.indices[customer]

        for block in blocks:
            for block_customer in block.customers:
                if self.indices[block_customer] == to_idx and is_pickup \
                        or self.indices[block_customer] < to_idx:
                    stack.push_rear(problem.pickups[block_customer])
                else:
                    stack.push_rear(problem.demands[block_customer])

        return stack
