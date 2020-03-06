from typing import List

from heuristic.classes import Problem, Route
from .Block import Block


def split(customers: List[int], num_partitions: int):
    """
    Splits the given list of customers into num_partitions partitions of roughly
    equal weight. Based on the answer given here:
    https://stackoverflow.com/a/35518541/4316405
    """
    problem = Problem()

    chunks_yielded = 0
    average_sum = Block(customers).max_capacity_used()
    avg_sum = average_sum / num_partitions
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

        customer_weight = max(problem.demands[customer].volume,
                              problem.pickups[customer].volume)

        seen += customer_weight

        if chunk_sum < avg_sum:
            chunk.append(customer)
            chunk_sum += customer_weight
        else:
            yield chunk

            # update average expected sum, because the last yielded chunk was
            # probably not perfect:
            avg_sum = (average_sum - seen) / (to_yield - 1)
            chunks_yielded += 1
            chunk_sum = customer_weight
            chunk = [customer]
