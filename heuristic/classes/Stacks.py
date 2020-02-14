from __future__ import annotations
from typing import List
from .Problem import Problem
from .Stack import Stack


class Stacks:
    _stacks: List[Stack]

    @classmethod
    def create(cls, nr_stacks) -> Stacks:
        stacks = cls()
        stacks._stacks = [Stack.create(Problem.stack_capacity) for idx in
                          range(nr_stacks)]

        return stacks

    def shortest_stack(self) -> int:
        """
        Returns the index of the shortest stack.
        """
        index = min(range(len(self._stacks)),
                    key=lambda idx:
                    self._stacks[idx].length_items_to_be_moved())
        return index


