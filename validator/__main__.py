import sys

from heuristic.classes import Problem, Solution
from .rules import RULES


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1], delimiter=',')
    solution = Solution.from_file(problem,
                                  f"solutions/oracs_{problem.instance}.csv")

    is_feasible = True

    for idx, rule in enumerate(RULES):
        result, message = rule(solution)

        print(f"{idx}: {message}")

        if not result:
            is_feasible = False

    exit(0 if is_feasible else 1)


if __name__ == "__main__":
    main()
