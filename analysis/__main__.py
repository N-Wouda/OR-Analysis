import glob
import sys

import pandas as pd

from heuristic.classes import Problem, Solution
from .statistics import STATISTICS


def main():
    """
    Prints several statistics of each instance and descriptive
    statistics of the instances overall to a file.
    """
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    cumulative_df = pd.DataFrame()

    for instance in glob.glob(sys.argv[1]):
        problem = Problem.from_file(instance, delimiter=',')
        solution = Solution.from_file(f"solutions/oracs_{problem.instance}.csv")
        instance_df = pd.DataFrame()

        for statistic in STATISTICS:
            statistic_value = statistic(solution)
            instance_df[statistic_value[0]] = [statistic_value[1]]

        cumulative_df = pd.concat([cumulative_df, instance_df])

        problem.clear()
        del problem

    cumulative_df.set_index('instance', inplace=True)
    cumulative_df.sort_index(inplace=True)

    cumulative_df.to_csv("statistics/summary.csv", sep='\t')
    cumulative_df.describe().\
        to_csv("statistics/summary.csv", mode='a', sep='\t')


if __name__ == "__main__":
    main()
