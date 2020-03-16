from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def same_number_in_vehicle(problem: Problem, solver):
    """
    Ensures the same number of items are in the truck at all points.
    """
    for customer_1 in range(1, problem.num_customers):
        before_customer = solver.sum(
            solver.demand_volume[customer_1, customer_2, stack, index] +
            solver.pickup_volume[customer_1, customer_2, stack, index]
            for customer_2 in range(problem.num_customers)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
        )
        after_customer = solver.sum(
            solver.demand_volume[customer_2, customer_1, stack, index] +
            solver.pickup_volume[customer_2, customer_1, stack, index]
            for customer_2 in range(problem.num_customers)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
        )

        solver.add_constraint(before_customer == after_customer)
