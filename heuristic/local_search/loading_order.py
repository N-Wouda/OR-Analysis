from numpy.random import RandomState

from heuristic.classes import Solution


def loading_order(current: Solution, rnd_state: RandomState) -> Solution:

    for route in current.routes:
        route.sort_start()
        route.sort_rest()

    return current
