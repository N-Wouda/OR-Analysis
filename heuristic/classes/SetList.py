from typing import List, Set, TypeVar

_T = TypeVar('_T')


class SetList(List[_T]):
    _set: Set[_T]

    def __init__(self, *args, **kwargs):
        """
        SetList is a hash set and array data structure, that supports the usual
        array-based operations, and O(1) look-ups.
        """
        super().__init__(*args, **kwargs)

        self._set = set(*args, **kwargs)

    def __contains__(self, item: _T):
        return item in self._set

    def append(self, obj: _T):
        super().append(obj)
        self._set.add(obj)

    def insert(self, index: int, obj: _T):
        self._set.add(obj)
        super().insert(index, obj)

    def remove(self, obj: _T):
        super().remove(obj)
        self._set.remove(obj)

    def __delitem__(self, index: int):
        self._set.remove(self[index])
        super().__delitem__(index)

    def __setitem__(self, index: int, value: _T):
        self._set.remove(self[index])
        self._set.add(value)

        super().__setitem__(index, value)
