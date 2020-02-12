from classes import Problem
import sys


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1], delimiter=',')

    # TODO


if __name__ == "__main__":
    main()
