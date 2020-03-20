from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickup_total(problem: Problem, solver):
    """
    Total pickups on truck on more after customer.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        pickups_from_customer = solver.sum(
            solver.pickup_binary[
                customer_1, customer_2, stack, index, 0, origin] -
            solver.pickup_binary[
                customer_2, customer_1, stack, index, 0, origin]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
            for origin in range(problem.num_customers + 1))
        solver.add_constraint(pickups_from_customer == 1)
