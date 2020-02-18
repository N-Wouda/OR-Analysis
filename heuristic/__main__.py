import sys

from alns import ALNS
from numpy.random import RandomState

from .classes import Problem
from .constants import CRITERION, DECAY, WEIGHTS
from .destroy_operators import D_OPERATORS
from .initial_solution import initial_solution
from .repair_operators import R_OPERATORS


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1], delimiter=',')
    init = initial_solution(problem)

    alns = ALNS(RandomState(problem.instance))

    for d_op in D_OPERATORS:
        alns.add_destroy_operator(d_op)

    for r_op in R_OPERATORS:
        alns.add_repair_operator(r_op)

    result = alns.iterate(init, WEIGHTS, DECAY, CRITERION, iterations=100)
    # TODO post-processing?

    result.best_state.to_file(f"solutions/oracs_{problem.instance}.csv")


if __name__ == "__main__":
    main()
