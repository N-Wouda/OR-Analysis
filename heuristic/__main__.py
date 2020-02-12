import sys

from .classes import Problem
from .initial_solution import initial_solution


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1], delimiter=',')
    init = initial_solution(problem)

    # TODO ALNS, post-processing?

    init.to_file(f"data/oracs_{problem.instance}.csv")


if __name__ == "__main__":
    main()
