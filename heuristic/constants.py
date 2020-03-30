import os

from alns.criteria import RecordToRecordTravel, SimulatedAnnealing

DEPOT = -1
TEAM_NUMBER = 3

if "TRAVIS" in os.environ:
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.2
    WEIGHTS = [25, 5, 1, 1]
    DECAY = 0.6

    ITERATIONS = 1000
    CRITERION = RecordToRecordTravel(200, 0, step=200 / ITERATIONS)
else:
    # Use these to play around with - the above is for Travis runs, and should
    # not be changed too much.
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.1
    WEIGHTS = [25, 10, 1, 0.8]
    DECAY = 0.9

    ITERATIONS = 25000
    CRITERION = SimulatedAnnealing(2000, 1, 0.999696, method="exponential")
