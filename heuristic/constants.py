from alns.criteria import RecordToRecordTravel

DEPOT = -1
TEAM_NUMBER = 3
DEGREE_OF_DESTRUCTION = 0.25
WEIGHTS = [25, 5, 1, 1]
DECAY = 0.8
ITERATIONS = 25000
CRITERION = RecordToRecordTravel(200, 1, step=199 / ITERATIONS)
