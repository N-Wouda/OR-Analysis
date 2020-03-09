from typing import List, Union

from heuristic.classes import Problem, SetList
from .Block import Block


def split(customers: Union[List[int], SetList[int]], num_partitions: int):
    """
    Splits the given list of customers into num_partitions partitions of
    roughly equal weight.

    Based on https://stackoverflow.com/a/35518541/4316405.
    """
    problem = Problem()

    chunks_yielded = 0
    total_sum = Block(customers).max_capacity_used()
    average_sum = total_sum / num_partitions
    chunk = []
    chunk_sum = 0
    seen = 0

    for idx, customer in enumerate(customers):
        if num_partitions - chunks_yielded == 1:
            yield chunk + customers[idx:]
            break

        to_yield = num_partitions - chunks_yielded
        chunks_left = len(customers) - idx

        if to_yield > chunks_left:
            if chunk:
                yield chunk

            yield from ([x] for x in customers[idx:])
            break

        max_customer_volume = max(problem.demands[customer].volume,
                                  problem.pickups[customer].volume)

        seen += max_customer_volume

        if chunk_sum < average_sum:
            chunk.append(customer)
            chunk_sum += max_customer_volume
        else:
            yield chunk

            # Update average expected sum, since the last yielded chunk was
            # probably not perfect.
            average_sum = (total_sum - seen) / (to_yield - 1)
            chunks_yielded += 1
            chunk_sum = max_customer_volume
            chunk = [customer]
