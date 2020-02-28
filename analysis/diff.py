import pandas as pd

from .functions import make_pivot_table, get_names
from .statistics import STATISTICS


def diff(first: str, second: str):
    """
    Displays the element-wise difference between the first and second
    statistics files. Second is subtracted from first.
    """
    data1 = pd.read_csv(first, skipfooter=1, engine="python")
    data2 = pd.read_csv(second, skipfooter=1, engine="python")

    assert len(data1) == len(data2)

    stats = get_names(STATISTICS)
    data1[stats] = data1[stats] - data2[stats]

    print(make_pivot_table(data1))
