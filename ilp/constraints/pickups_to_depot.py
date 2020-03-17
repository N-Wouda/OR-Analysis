from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickups_to_depot(problem: Problem, solver):
    """
    Ensures customer pickups are delivered to depot.
"""
    total_pickup = solver.sum(
        solver.pickup_volumes[customer, 0, stack, index]
        for customer in range(problem.num_customers)
        for stack in range(problem.num_stacks)
        for index in range(MAX_STACK_INDEX))

    total_pickup_volume = sum(problem.pickups[customer].volume for customer in
                              range(problem.num_customers))

    solver.add_constraint(total_pickup == total_pickup_volume)
