from heuristic.classes import Heap, Problem, Route, Solution
from heuristic.constants import DEPOT
from heuristic.functions import remove_empty_routes, routing_costs


def cross_customer_exchange(solution: Solution) -> Solution:
    """
    Tries to remove crossing links between routes.
    TODO neighbourhood size
    TODO best move? First better?

    References
    ----------
    - Savelsbergh, Martin W. P. 1992. "The Vehicle Routing Problem with Time
      Windows: Minimizing Route Duration." *ORSA Journal on Computing* 4 (2):
      146-154.
    """

    return solution
