from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def handling_costs(problem: Problem, solver):
    """
    Sets handling costs.
    """
    for customer_1 in range(problem.num_customers):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                demand_cost = \
                    solver.sum(problem.demands[destination - 1].volume *
                               solver.demand_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    destination,
                                                    0]
                               for customer_2 in
                               range(problem.num_customers + 1)
                               for destination in
                               range(1, problem.num_customers + 1))

                pickup_cost = \
                    solver.sum(problem.pickups[origin - 1].volume *
                               solver.pickup_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    0,
                                                    origin]
                               for customer_2 in
                               range(problem.num_customers + 1)
                               for origin in
                               range(1, problem.num_customers + 1))

                not_moved_reduction = M * (
                        1 - solver.is_moved[customer_1, stack, index])

                handling_value = solver.max(demand_cost +
                                            pickup_cost -
                                            not_moved_reduction,
                                            0)

                solver.add_constraint(
                    solver.handling_cost[customer_1, stack, index]
                    >= handling_value)
