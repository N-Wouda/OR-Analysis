from heuristic.classes import Problem
from heuristic.constants import M, MAX_STACK_INDEX


def handling_costs(problem: Problem, solver):
    """
    Sets handling costs.
    """
    for customer_1 in range(problem.num_customers + 1):
        for stack in range(problem.num_stacks):
            for index in range(MAX_STACK_INDEX):
                demand = 0
                demand_cost = \
                    solver.sum(problem.demands[destination - 1].volume *
                               solver.demand_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    destination,
                                                    origin]
                               for customer_2 in
                               range(problem.num_customers + 1)
                               for destination in
                               range(1, problem.num_customers + 1)
                               for origin in
                               range(problem.num_customers + 1)
                               if customer_1 is not destination)
                pickup_cost = 0
                pickup_cost = \
                    solver.sum(problem.pickups[origin - 1].volume *
                               solver.pickup_binary[customer_1,
                                                    customer_2,
                                                    stack,
                                                    index,
                                                    destination,
                                                    origin]
                               for customer_2 in
                               range(problem.num_customers + 1)
                               for destination in
                               range(problem.num_customers + 1)
                               for origin in
                               range(1, problem.num_customers + 1)
                               if customer_1 is not origin)

                not_moved_reduction = M * (
                        1 - solver.is_moved[customer_1, stack, index])

                handling_value = demand_cost + pickup_cost - not_moved_reduction
                # handling_value = (demand_cost + pickup_cost) * solver.is_moved[customer_1, stack, index]

                solver.add_constraint(
                    solver.handling_cost[customer_1, stack, index]
                    >= handling_value)
