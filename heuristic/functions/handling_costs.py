import numpy as np

from heuristic.classes import Problem, Solution, Stacks


def handling_costs(sol: Solution) -> np.ndarray:
    """
    Computes handling costs for each customer. This is an approximation: only
    the handling costs *at* the customer are computed, any costs made at other
    legs of the tour are not considered. O(|customers|).

    Note: this is an approximation for the actual handling costs, as those are
    rather hard to compute. The approximation is a lower bound, but generally
    quite a good one.
    """
    problem = Problem()
    costs = np.zeros(problem.num_customers)

    for route in sol.routes:
        indices = {customer: idx for idx, customer
                   in enumerate(route.customers)}

        for idx, customer in enumerate(route.customers):
            delivery = problem.demands[customer]
            pickup = problem.pickups[customer]

            before, after = route.plan[idx], route.plan[idx + 1]

            # This is the handling cost for just this customer.
            costs[customer] += Stacks.cost(customer, before, after)

            # This is the handling cost due to the customer's delivery item, as
            # the number of times it must be moved to take out delivery items
            # for customers visited earlier on in the route.
            stack = route.plan[0].find_stack(delivery)
            volume = 0.

            for item in reversed(stack):
                if item.customer == customer:
                    break

                # The delivery item is moved only when this item's customer
                # precedes our current customer
                volume += (indices[item.customer] < idx) * delivery.volume

            # This is the handling cost incurred by the customer's pick-up
            # item. It counts the number of times the pickup item needs to be
            # moved due to deliveries, but e.g. not the number of times it is
            # moved because a pick-up item was inserted before it.
            stack = after.find_stack(pickup)

            if stack[0].customer == customer:
                # This is only relevant if the item was inserted in the rear
                # - else this has already been accounted for in the general
                # cost computation.
                volume += stack.deliveries_in_stack() * pickup.volume

            costs[customer] += problem.handling_cost * volume

    return costs
