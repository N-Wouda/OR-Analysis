import argparse

import pandas as pd

from .analyse import analyse
from .diff import diff

pd.set_option('display.float_format', "{:.2f}".format)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def main():
    parser = argparse.ArgumentParser(description="Analyses heuristic outputs.")

    parser.add_argument("input",
                        help="Input data file locations (glob string).")

    parser.add_argument("output",
                        help="Output data location.")

    parser.add_argument("--diff", action="store_true", dest="diff",
                        help="Displays the difference between two analyses"
                             " result files. Second file is subtracted from"
                             " the first.")

    args = parser.parse_args()

    if args.diff:
        diff(args.input, args.output)
    else:
        analyse(args.input, args.output)


if __name__ == "__main__":
    main()
