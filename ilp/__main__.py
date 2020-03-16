import sys

from heuristic.classes import Problem, Solution
from .ilp import ilp


def main():
    problem = Problem.from_file(sys.argv[1], delimiter=',')
    solution = ilp(problem)

    # write_result(result, MethodType.ILP, sys.argv[1], sys.argv[2])
    # solution.to_file(f"solutions/ILP_{problem.instance}.csv")


if __name__ == "__main__":
    main()