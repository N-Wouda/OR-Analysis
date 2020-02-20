from heuristic.classes import Item, Problem, Route, Stacks
from heuristic.constants import DEPOT


def create_single_customer_route(customer: int) -> Route:
    """
    Creates a single customer route for the passed-in customer. This route
    visits the DEPOT, then the customer, and returns to the DEPOT. O(1).
    """
    problem = Problem()

    # After depot, and after customer: two configurations in total.
    stacks = [Stacks(problem.num_stacks) for _ in range(2)]

    # We place the deliveries and pickups in the shortest stack - this
    # does not really matter much, as each stack is empty at this point
    # anyway.
    stacks[0].shortest_stack().push_rear(problem.demands[customer])
    stacks[1].shortest_stack().push_rear(problem.pickups[customer])

    return Route([customer], stacks)
