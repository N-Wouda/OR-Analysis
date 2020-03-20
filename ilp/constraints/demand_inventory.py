from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demand_inventory(problem: Problem, solver):
    """
    Ensures demand items are in the truck before and after a customer, if it is
    not delivered to this customer.
    """
    for customer_1 in range(1, problem.num_customers + 1):
        for destination in range(problem.num_customers + 1):
            if customer_1 is not destination:
                demand_to_customer = solver.sum(
                    solver.demand_binary[
                        customer_2, customer_1, stack, index, destination, 0]
                    for customer_2 in range(problem.num_customers + 1)
                    for stack in range(problem.num_stacks)
                    for index in range(MAX_STACK_INDEX))

                demand_after_customer = solver.sum(
                    solver.demand_binary[
                        customer_1, customer_2, stack, index, destination, 0]
                    for customer_2 in range(problem.num_customers + 1)
                    for stack in range(problem.num_stacks)
                    for index in range(MAX_STACK_INDEX))

            solver.add_constraint(demand_to_customer == demand_after_customer)
