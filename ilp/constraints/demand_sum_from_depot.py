from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def demand_sum_from_depot(problem: Problem, solver):
    """
    Ensures customer pickups are delivered to depot. kan ook zonder volume
    TODO in paper zetten.
    """
    total_demand = solver.sum(
        solver.demand_binary[0, customer, stack, index, destination, 0] *
        problem.demands[destination - 1].volume
        for customer in range(1, problem.num_customers + 1)
        for stack in range(problem.num_stacks)
        for index in range(MAX_STACK_INDEX)
        for destination in range(1, problem.num_customers + 1))

    total_demand_volume = sum(problem.demands[customer].volume for customer in
                              range(problem.num_customers))

    solver.add_constraint(total_demand == total_demand_volume)
