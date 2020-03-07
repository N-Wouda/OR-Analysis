from alns.criteria import RecordToRecordTravel

DEPOT = -1
TEAM_NUMBER = 3
NUM_BLOCKS = 4
NEARNESS = 3
DEGREE_OF_DESTRUCTION = 0.2
WEIGHTS = [25, 5, 1, 1]
DECAY = 0.6
ITERATIONS = 1000
CRITERION = RecordToRecordTravel(250, 0, step=0.99995,
                                 method="exponential")
