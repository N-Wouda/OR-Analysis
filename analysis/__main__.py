import glob
import os
import pandas as pd


from heuristic.classes import Problem, Solution

from .statistics import STATISTICS


def main():
    cumulative_df = pd.dataframe()

    for idx, instance in enumerate(glob.glob("oracs_*.csv")):
        solution = Solution.from_file(f"solutions/oracs_{instance}.csv")
        problem = Problem.from_file(f"~data/small_{instance}", delimiter=',')

        instance_df = pd.dataframe()

        for statistic in STATISTICS:
            statistic_value = statistic(solution)
            cumulative_df[statistic_value[0]] = statistic_value[1]

        cumulative_df = pd.concat([cumulative_df, instance_df])

        del problem

    cumulative_df.set_index('instance', inplace=True)

    os.chdir = "~OR-Analysis/statistics"
    file = open("summary.csv", 'w+')
    print(cumulative_df)
    print(cumulative_df.describe())
    file.close()


if __name__ == "__main__":
    main()
