from dataclasses import dataclass
from typing import List


@dataclass
class Block:
    """
    A block of customers. This groups several customers together, that are
    moved around by the MDP (as an approximation to the optimal handling
    policy, which would move each customer individually).
    """
    customers: List[int]

    def __iter__(self):
        yield from self.customers
