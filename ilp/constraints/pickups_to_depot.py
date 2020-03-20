from heuristic.classes import Problem
from heuristic.constants import MAX_STACK_INDEX


def pickups_to_depot(problem: Problem, solver):
    """
    Ensures customer pickups are delivered to depot.
    # TODO in paper zetten indien nodig.
    """
    total_pickup = solver.sum(problem.pickups[origin - 1].volume *
                              solver.pickup_binary[
                                  customer, 0, stack, index, 0, origin]
                              for customer in range(problem.num_customers + 1)
                              for stack in range(problem.num_stacks)
                              for index in range(MAX_STACK_INDEX)
                              for origin in range(problem.num_customers + 1))

    total_pickup_volume = sum(problem.pickups[customer].volume for customer in
                              range(problem.num_customers))

    solver.add_constraint(total_pickup == total_pickup_volume)
