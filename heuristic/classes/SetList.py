from typing import Generic, List, Set, TypeVar

_T = TypeVar('_T')


class SetList(Generic[_T]):
    _list: List[_T]
    _set: Set[_T]

    def __init__(self, *args, **kwargs):
        """
        SetList is a hash set and array data structure, that supports the usual
        array-based operations, and O(1) look-ups.

        Note: this data structure must *not* be used for data that may contain
        duplicates. Furthermore, it is not complete and should be extended
        as-needed.
        """
        self._list = list(*args, **kwargs)
        self._set = set(*args, **kwargs)

    def __contains__(self, item: _T) -> bool:
        return item in self._set

    def __len__(self) -> int:
        return len(self._list)

    def __iter__(self):
        yield from self._list

    def append(self, obj: _T):
        self._list.append(obj)
        self._set.add(obj)

    def index(self, obj: _T) -> int:
        return self._list.index(obj)

    def insert(self, index: int, obj: _T):
        self._list.insert(index, obj)
        self._set.add(obj)

    def remove(self, obj: _T):
        self._list.remove(obj)
        self._set.remove(obj)

    def __delitem__(self, index: int):
        item = self._list[index]

        del self._list[index]
        self._set.remove(item)

    def __getitem__(self, index: int) -> _T:
        return self._list[index]

    def __setitem__(self, index: int, value: _T):
        curr = self._list[index]

        self._list[index] = value

        self._set.remove(curr)
        self._set.add(value)

    def to_list(self) -> List[_T]:
        return self._list

    def to_set(self) -> Set[_T]:
        return self._set
