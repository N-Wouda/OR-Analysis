import sys

from heuristic.classes import Problem, Solution
from .ilp import ilp


def main():
    problem = Problem.from_file(sys.argv[1], delimiter=',')

    # noinspection PyTypeChecker
    solution: Solution = ilp(problem)

    print(solution.routes)

    solution.to_file(f"solutions/oracs_ILP_{problem.instance}.csv")

    import matplotlib.pyplot as plt
    solution.plot()
    plt.show()

    print(solution.objective())


if __name__ == "__main__":
    main()
