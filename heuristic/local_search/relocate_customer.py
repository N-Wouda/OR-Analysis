from heuristic.classes import Heap, Problem, Route, Solution
from heuristic.constants import DEPOT
from heuristic.functions import remove_empty_routes, routing_costs


@remove_empty_routes
def relocate_customer(solution: Solution) -> Solution:
    """
    Performs the best customer relocation move, that is, a customer is
    reassigned to a different route. Of all such moves, the best is performed
    and the updated solution is returned. O(n^2), where n is the number of
    customers.

    References
    ----------
    - Savelsbergh, Martin W. P. 1992. "The Vehicle Routing Problem with Time
      Windows: Minimizing Route Duration." *ORSA Journal on Computing* 4 (2):
      146-154.
    """
    problem = Problem()

    insert_locations = Heap()

    routing = routing_costs(solution)

    for customer in range(problem.num_customers):
        for route in solution.routes:
            for idx in range(len(route.customers) + 1):
                if not route.can_insert(customer, idx):
                    continue

                pred = DEPOT if idx == 0 else route.customers[idx - 1]
                succ = DEPOT if idx == len(route.customers) else route.customers[idx]

                gain = Route.distance([pred, customer, succ])
                gain -= routing[customer]

                if gain < 0:
                    insert_locations.push(gain, (customer, idx, route))

    while len(insert_locations) != 0:
        # We do not check for the handling effects here - although that is of
        # course a serious consideration, getting customers into the proper
        # routes counts a lot more at the solution level. The route based
        # operators will likely repair any inefficiencies due to handling.
        _, (customer, insert_idx, next_route) = insert_locations.pop()

        # TODO this does not work for small instances, because some routes
        #  turn empty once the customer is removed (insertion then has an
        #  index that's too large). Think about how to fix.

        route = solution.find_route(customer)
        route.remove_customer(customer)

        next_route.insert_customer(customer, insert_idx)

    return solution
