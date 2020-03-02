from alns.criteria import RecordToRecordTravel

DEPOT = -1
TEAM_NUMBER = 3
NUM_BLOCKS_PER_STACK = 2
DEGREE_OF_DESTRUCTION = 0.2
WEIGHTS = [25, 5, 1, 1]
DECAY = 0.6
ITERATIONS = 1000
CRITERION = RecordToRecordTravel(200, 1, step=199 / ITERATIONS)
