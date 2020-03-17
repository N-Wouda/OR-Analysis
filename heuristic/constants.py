import os

from alns.criteria import RecordToRecordTravel
from .RestartingRRT import RestartingRRT

DEPOT = -1
TEAM_NUMBER = 3

if "TRAVIS" in os.environ:
    MAX_OPT_ROUTE_LENGTH = 10
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.2
    WEIGHTS = [25, 5, 1, 1]
    DECAY = 0.6

    ITERATIONS = 1000
    CRITERION = RecordToRecordTravel(200, 0, step=200 / ITERATIONS)
else:
    # Use these to play around with - the above is for Travis runs, and should
    # not be changed too much.
    MAX_OPT_ROUTE_LENGTH = 25
    NEARNESS = 3
    DEGREE_OF_DESTRUCTION = 0.2
    WEIGHTS = [25, 5, 1, 1]
    DECAY = 0.6

    ITERATIONS = 25000
    CRITERION = RestartingRRT(5000, 200, 1, step=200 / 4000)
