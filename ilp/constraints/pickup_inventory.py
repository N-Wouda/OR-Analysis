from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickup_inventory(problem: Problem, solver):
    """
    Ensures pickup items are in the truck before and after a customer, if it is
    not delivered to this customer.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        for origin in range(1, problem.num_customers + 1):
            if customer_1 is not origin:
                pickup_to_customer = solver.sum(
                    solver.pickup_binary[
                        customer_2, customer_1, stack, index, 0, origin]
                    for customer_2 in range(problem.num_customers + 1)
                    for stack in range(problem.num_stacks)
                    for index in range(MAX_STACK_INDEX))

                pickup_after_customer = solver.sum(
                    solver.pickup_binary[
                        customer_1, customer_2, stack, index, 0, origin]
                    for customer_2 in range(problem.num_customers + 1)
                    for stack in range(problem.num_stacks)
                    for index in range(MAX_STACK_INDEX))

                solver.add_constraint(
                    pickup_to_customer == pickup_after_customer)
