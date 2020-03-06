from collections import defaultdict
from typing import List

from heuristic.classes import Problem, Route
from heuristic.constants import NUM_BLOCKS
from .Block import Block
from .split import split


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

    blocks = []

    # Create NUM_BLOCKS_PER_STACK blocks for each stack by balancing the
    # customer item sizes between blocks.
    for idx, stack in _customers_by_stack(route):
        for customers in split(stack, NUM_BLOCKS // problem.num_stacks):
            blocks.append(Block(customers))

    while len(blocks) != NUM_BLOCKS:
        largest = max(blocks, key=lambda block: block.max_capacity_used())

        blocks.remove(largest)
        blocks.extend(largest.split())

    assert len(blocks) == NUM_BLOCKS
    return blocks


def _customers_by_stack(route: Route):
    problem = Problem()

    by_stack = defaultdict(list)

    for customer in route.customers:
        # Find the stack the customer's items are assigned to at the depot. We
        # will use this to determine the block assignments.
        stack = route.plan[0].find_stack(problem.demands[customer])
        by_stack[stack.index].append(customer)

    # There's no point in returning an empty stack - we might just as well
    # skip it here.
    return [(idx, customers) for idx, customers in by_stack.items()
            if len(customers) != 0]
