from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickup(problem: Problem, solver):
    """
    Ensures customer pickups are picked up.
    """
    for customer_1 in range(1, problem.num_customers):
        pickups_from_customer = solver.sum(
            solver.pickup_binary[
                customer_1, customer_2, stack, index, destination] -
            solver.pickup_binary[
                customer_2, customer_1, stack, index, destination]
            for destination in range(problem.num_customers)
            for customer_2 in range(problem.num_customers)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX))
        solver.add_constraint(pickups_from_customer == 1)
