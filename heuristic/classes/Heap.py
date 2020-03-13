import heapq
from typing import List, Tuple, TypeVar

_T = TypeVar("_T")


class Heap:
    _data: List[Tuple[float, int, _T]]

    def __init__(self):
        self._data = []

    def __len__(self) -> int:
        return len(self._data)

    def push(self, key: float, item: _T):
        # See https://stackoverflow.com/a/8875823/4316405 for a comment
        # on the use of id() here.
        heapq.heappush(self._data, (key, id(item), item))

    def pop(self) -> Tuple[float, _T]:
        key, _, item = heapq.heappop(self._data)
        return key, item

    def nsmallest(self, num_smallest: int) -> List[Tuple[float, _T]]:
        result = heapq.nsmallest(num_smallest, self._data)
        return [(cost, item) for cost, _, item in result]
