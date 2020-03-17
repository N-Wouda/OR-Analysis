import sys

from alns import ALNS
from numpy.random import RandomState

from heuristic.classes import Solution
from .classes import Problem
from .constants import CRITERION, DECAY, ITERATIONS, WEIGHTS
from .destroy_operators import D_OPERATORS
from .functions import initial_solution
from .local_search import LocalSearch
from .repair_operators import R_OPERATORS


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1], delimiter=',')

    alns = ALNS(RandomState(problem.instance))

    for op in D_OPERATORS:
        alns.add_destroy_operator(op)

    for op in R_OPERATORS:
        alns.add_repair_operator(op)

    alns.on_best(LocalSearch())

    init = initial_solution()
    result = alns.iterate(init, WEIGHTS, DECAY, CRITERION, ITERATIONS)
    # TODO post-processing?

    # noinspection PyTypeChecker
    solution: Solution = result.best_state

    solution.to_file(f"solutions/oracs_{problem.instance}.csv")

    # print(solution.routes[0])

    import matplotlib.pyplot as plt
    result.best_state.plot()
    plt.show()

    _, ax = plt.subplots(figsize=(12, 6))
    result.plot_objectives(ax=ax, lw=2)
    plt.show()


if __name__ == "__main__":
    main()
