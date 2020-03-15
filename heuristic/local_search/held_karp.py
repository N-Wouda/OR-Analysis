from itertools import combinations
from typing import List

import numpy as np


def held_karp(distances: np.ndarray) -> List[int]:
    """
    The Held-Karp shortest tour of this set of customers. For each customer C,
    find the shortest segment from DEPOT (the start) to C. Out of all these
    shortest segments, pick the one that is the shortest tour.

    O(2^n n^2), with n the number of customers. Taken largely from the code at
    https://github.com/CarlEkerot/held-karp, which is fairly efficient.
    """
    n = len(distances)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    costs = {}

    # Set transition cost from initial state
    for k in range(1, n):
        costs[1 << k, k] = (distances[0, k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0

            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)
                res = []

                for m in subset:
                    if m == 0 or m == k:
                        continue

                    res.append((costs[prev, m][0] + distances[m, k], m))

                costs[bits, k] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2 ** n - 1) - 1

    # Calculate optimal cost
    opt, parent = min((costs[bits, k][0] + distances[k, 0], k)
                      for k in range(1, n))

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = costs[bits, parent]
        bits = new_bits

    return path
