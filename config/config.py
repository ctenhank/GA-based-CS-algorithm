import json

class Config:
    # IDs for assignment
    CNT_APP: int = 0
    CNT_MS: int = 0
    CNT_CONT: int = 0
    CNT_PM: int = 0

    # Execution parameters based on the [3].
    NUM_POPULATION: int = 200
    NUM_MUTATION: int = 0
    NUM_GENERATION: int = 300
    PROB_MUTATION: float = 0.25
    PROB_MUTATION_SELECTION: float = 1/3
    PROB_CROSSOVER : float = 1.0

config = json.dumps(Config())