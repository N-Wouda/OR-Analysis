import os

from alns.criteria import RecordToRecordTravel

DEPOT = -1
TEAM_NUMBER = 3

if "TRAVIS" in os.environ:
    NUM_BLOCKS = 4
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.2
    WEIGHTS = [25, 5, 1, 1]
    DECAY = 0.6

    ITERATIONS = 1000
    CRITERION = RecordToRecordTravel(200, 0, step=200 / ITERATIONS)
else:
    # Use these to play around with - the above is for Travis runs, and should
    # not be changed too much.
    NUM_BLOCKS = 4
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.2
    WEIGHTS = [25, 5, 1, 1]
    DECAY = 0.6

    ITERATIONS = 25000
    CRITERION = RecordToRecordTravel(250, 0, step=0.99995,
                                     method="exponential")
