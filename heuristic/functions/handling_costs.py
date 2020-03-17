import numpy as np

from heuristic.classes import Problem, Solution, Stacks


def handling_costs(sol: Solution) -> np.ndarray:
    """
    Computes handling costs for each customer. This is an approximation: only
    the handling costs *at* the customer are computed, any costs made at other
    legs of the tour are not considered. O(|customers|).

    Note: this is a lower bound on the actual handling costs, as those are
    rather hard to compute. Some experimentation suggests it is e.g. not
    worthwhile to also count the costs incurred due to the delivery item.
    """
    problem = Problem()
    costs = np.zeros(problem.num_customers)

    for route in sol.routes:
        for idx, customer in enumerate(route.customers):
            before, after = route.plan[idx], route.plan[idx + 1]

            # This is the handling cost for just this customer.
            costs[customer] += Stacks.cost(customer, before, after)

            # These are the handling costs incurred by the customer's pick-up
            # item. It counts the number of times the pickup item needs to be
            # moved due to deliveries, but e.g. not the number of times it is
            # moved because a pick-up item was inserted before it.
            pickup = problem.pickups[customer]
            stack = after.find_stack(pickup)

            if stack[0].customer == customer:
                # This is only relevant if the item was inserted in the rear
                # - else this has already been accounted for in the general
                # cost computation.
                volume = stack.deliveries_in_stack() * pickup.volume
                costs[customer] += problem.handling_cost * volume

    return costs
