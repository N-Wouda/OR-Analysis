from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def total_items(problem: Problem, solver):
    """
    Ensures the total number of items going and coming from the depot is
    equal to the number of customers.
    # TODO in paper zetten indien nodig. Ik denk dat deze niet nodig is
    """
    from_depot = solver.sum(
        solver.demand_binary[0, customer, stack, index, destination, 0] +
        solver.pickup_binary[0, customer, stack, index, 0, destination]
        for destination in range(problem.num_customers)
        for customer in range(problem.num_customers)
        for stack in range(problem.num_stacks)
        for index in range(MAX_STACK_INDEX)
    )

    solver.add_constraint(from_depot == problem.num_customers)

    to_depot = solver.sum(
        solver.demand_binary[customer, 0, stack, index, destination, 0] +
        solver.pickup_binary[customer, 0, stack, index, 0, destination]
        for destination in range(problem.num_customers)
        for customer in range(problem.num_customers)
        for stack in range(problem.num_stacks)
        for index in range(MAX_STACK_INDEX)
    )

    solver.add_constraint(to_depot == problem.num_customers)
