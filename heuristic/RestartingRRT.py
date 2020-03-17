from alns.criteria import AcceptanceCriterion, SimulatedAnnealing as RecordToRecordTravel


class RestartingRRT(AcceptanceCriterion):
    _criterion: RecordToRecordTravel

    _start: float
    _end: float
    _step: float
    _method: str

    _iterations: int
    _max_iterations: int

    def __init__(self,
                 max_iterations: int,
                 start: float,
                 end: float,
                 step: float,
                 method: str = "linear"):
        self._max_iterations = max_iterations

        self._start = start
        self._end = end
        self._step = step
        self._method = method

        self.reset()

    def accept(self, rnd, best, current, candidate):
        self._iterations += 1

        if self._iterations == self._max_iterations:
            self.reset()

        return self._criterion.accept(rnd, best, current, candidate)

    def reset(self):
        self._iterations = 0
        self._criterion = RecordToRecordTravel(self._start,
                                               self._end,
                                               self._step,
                                               self._method)
