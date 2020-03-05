from typing import List

import numpy as np

from heuristic.classes import Problem, Route
from .Block import Block
from heuristic.constants import NUM_BLOCKS_PER_STACK


def make_blocks(route: Route) -> List[Block]:
    """
    Constructs suitable blocks for the given route. These adhere to the single
    invariant that each block can be placed in each position, without violating
    stack capacity constraints (they are perfectly interchangeable).
    """
    # TODO clean this.
    problem = Problem()
    customers = route.customers

    if len(customers) <= NUM_BLOCKS_PER_STACK * problem.num_stacks:
        return [Block([customer]) for customer in customers]

    by_stack = [[] for _ in range(problem.num_stacks)]

    for customer in customers:
        # Find the stack the customer's items are assigned to at the depot. We
        # will use this to determine the block assignments.
        stack = route.plan[0].find_stack(problem.demands[customer])
        by_stack[stack.index].append(customer)

    # Max possible capacity use for having customer in the stack. This will
    # be used below to determine the block boundaries, such that each block
    # fits at each block location in the vehicle.
    max_size = [np.cumsum([max(problem.demands[customer].volume,
                               problem.pickups[customer].volume)
                          for customer in stack])
                for stack in by_stack]

    output = []

    # Create NUM_BLOCKS_PER_STACK blocks for each stack.
    # TODO re-allocate empty blocks over the other stacks.
    for idx, stack in enumerate(by_stack):
        if len(stack) == 0:
            output.extend([Block([]) for _ in range(NUM_BLOCKS_PER_STACK)])
            continue

        part_sum = max_size[idx][-1] // NUM_BLOCKS_PER_STACK
        cumulative = np.array(range(1, NUM_BLOCKS_PER_STACK)) * part_sum
        indices = np.searchsorted(max_size[idx], cumulative)

        output.extend([Block(customers)
                       for customers in np.split(stack, indices)])

    return output
