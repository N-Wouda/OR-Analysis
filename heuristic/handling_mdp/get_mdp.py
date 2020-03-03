import itertools

from heuristic.classes import Route
from .MDP import MDP
from .make_blocks import make_blocks


def get_mdp(route: Route) -> MDP:
    """
    Creates a simple MDP for the given route. This MDP consists of blocks, each
    containing some customers on the route. The MDP will solve the
    transportation plan for these blocks to optimality.
    """
    blocks = make_blocks(route)
    states = list(itertools.permutations(blocks))

    return MDP(states, route)
