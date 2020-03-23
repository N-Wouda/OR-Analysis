from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def same_number_in_vehicle(problem: Problem, solver):
    """
    Ensures the same number of items are in the truck at all points.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        before_customer_demand = solver.sum(
            solver.demand_binary[
                customer_1, customer_2, stack, index, destination]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
            for destination in range(problem.num_customers + 1)
        )
        before_customer_pickup = solver.sum(
            solver.pickup_binary[
                customer_1, customer_2, stack, index, origin]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
            for origin in range(problem.num_customers + 1)
        )
        after_customer_demand = solver.sum(
            solver.demand_binary[
                customer_2, customer_1, stack, index, destination]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
            for destination in range(problem.num_customers + 1)
        )
        after_customer_pickup = solver.sum(
            solver.pickup_binary[
                customer_2, customer_1, stack, index, origin]
            for customer_2 in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX)
            for origin in range(problem.num_customers + 1)
        )

        before_customer = before_customer_demand + before_customer_pickup
        after_customer = after_customer_demand + after_customer_pickup

        solver.add_constraint(before_customer == after_customer)
