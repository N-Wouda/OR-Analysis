import itertools

from heuristic.classes import Route
from .MDP import MDP
from .make_blocks import make_blocks


def get_mdp(route: Route) -> MDP:
    blocks = make_blocks(route)
    states = list(itertools.permutations(blocks))

    return MDP(states, route)
