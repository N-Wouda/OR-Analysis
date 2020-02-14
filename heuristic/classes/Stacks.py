from __future__ import annotations
from typing import List
from .Problem import Problem
from .Stack import Stack


class Stacks:
    _stacks: List[Stack]

    def __init__(self, nr_stacks: int):
        self._stacks = [Stack.create(Problem.stack_capacity) for idx in
                        range(nr_stacks)]

    def shortest_stack(self) -> Stack:
        """
        Returns the index of the shortest stack.
        """
        index = min(range(len(self._stacks)), key=lambda idx: self._stacks[idx])

        return index
