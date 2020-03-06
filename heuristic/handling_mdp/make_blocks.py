from typing import List

import numpy as np

from heuristic.classes import Problem, Route
from .Block import Block
from heuristic.constants import NUM_BLOCKS


def make_blocks(route: Route) -> List[Block]:
    """
    Constructs suitable blocks for the given route. These adhere to the single
    invariant that each block can be placed in each position, without violating
    stack capacity constraints (they are perfectly interchangeable).
    """
    problem = Problem()

    if len(route.customers) <= NUM_BLOCKS:
        blocks = [Block([]) for _ in range(NUM_BLOCKS - len(route.customers))]
        blocks.extend(Block([customer]) for customer in route.customers)

        assert len(blocks) == NUM_BLOCKS
        return blocks

    by_stack = _customers_by_stack(route)

    # Max possible capacity use for having customer in the stack. This will
    # be used below to determine the block boundaries, such that each block
    # fits at each block location in the vehicle.
    max_size = [np.cumsum([max(problem.demands[customer].volume,
                               problem.pickups[customer].volume)
                          for customer in stack])
                for stack in by_stack]

    blocks_per_stack = NUM_BLOCKS // problem.num_stacks
    blocks = []

    # Create NUM_BLOCKS_PER_STACK blocks for each stack. This is based on the
    # answer at https://stackoverflow.com/a/54024280/4316405, but might not be
    # all that great. TODO check if this can and needs to be improved.
    for idx, stack in enumerate(by_stack):
        if len(stack) != 0:
            part_sum = max_size[idx][-1] // blocks_per_stack
            cumulative = np.array(range(1, blocks_per_stack)) * part_sum
            indices = np.searchsorted(max_size[idx], cumulative)

            blocks.extend([Block(customers)
                           for customers in np.split(stack, indices)])

    while len(blocks) != NUM_BLOCKS:
        largest = max(blocks, key=lambda block: block.max_capacity_used())

        blocks.remove(largest)
        blocks.extend(largest.split())

    assert len(blocks) == NUM_BLOCKS
    return blocks


def _customers_by_stack(route: Route) -> List[List[int]]:
    problem = Problem()

    by_stack = [[] for _ in range(problem.num_stacks)]

    for customer in route.customers:
        # Find the stack the customer's items are assigned to at the depot. We
        # will use this to determine the block assignments.
        stack = route.plan[0].find_stack(problem.demands[customer])
        by_stack[stack.index].append(customer)

    return by_stack
