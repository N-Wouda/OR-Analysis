class Truck:
    capacity: int
    num_stacks: int

    def __init__(self, capacity: int, num_stacks: int):
        assert capacity > 0
        self.capacity = capacity

        assert num_stacks > 0
        self.num_stacks = num_stacks

    @property
    def stack_capacity(self) -> int:
        assert self.capacity % self.num_stacks == 0
        return self.capacity // self.num_stacks
