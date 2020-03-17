from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demands_from_depot(problem: Problem, solver):
    """
    Ensures customer pickups are delivered to depot.
    """
    total_demand = solver.sum(
        solver.demand_volumes[0, customer, stack, index]
        for customer in range(problem.num_customers)
        for stack in range(problem.num_stacks)
        for index in range(MAX_STACK_INDEX))

    total_demand_volume = sum(problem.demands[customer].volume for customer in
                              range(problem.num_customers))

    solver.add_constraint(total_demand == total_demand_volume)
