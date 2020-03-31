from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def total_items(problem: Problem, solver):
    """
    Ensures that each demand item comes from the depot and each pickup item is
    delivered to the depot.
    """

    # 1 demand item for each customer from the depot.
    for destintation in range(1, problem.num_customers + 1):
        demand_from_depot = solver.sum(
            solver.demand_binary[0, customer, stack, index, destintation]
            for customer in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX))
        solver.add_constraint(demand_from_depot == 1)

    #   1 pickup item from each customer to the depot.
    for origin in range(1, problem.num_customers + 1):
        pickup_to_depot = solver.sum(
            solver.pickup_binary[customer, 0, stack, index, origin]
            for customer in range(problem.num_customers + 1)
            for stack in range(problem.num_stacks)
            for index in range(MAX_STACK_INDEX))
        solver.add_constraint(pickup_to_depot == 1)
