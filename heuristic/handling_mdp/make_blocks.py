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
    stack capacity constraints (they are nearly completely interchangeable).
    """
    if len(route.customers) <= NUM_BLOCKS:
        # This we can solve optimally, with a block for each customer.
        blocks = [Block([]) for _ in range(NUM_BLOCKS - len(route.customers))]
        blocks.extend(Block([customer]) for customer in route.customers)
    else:
        # Create NUM_BLOCKS of customers by grouping nearby customers on the
        # route. These blocks are approximately balanced.
        blocks = list(map(Block, split(route.customers.to_list(), NUM_BLOCKS)))

    assert len(blocks) == NUM_BLOCKS
    return blocks
