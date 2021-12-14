
class Config:
    NUM_APP = 1
    NUM_PM = [250, 300, 350, 400]
    CUR_NUM_PM = 0

    PM_CAPABILITY = [100.0, 200.0, 400.0, 800.0]
    PM_FAILURE = 0.025

    DIST_NETWORK = [1.0, 4.0]
    RACK_TYPE = [0, 1]

    # Execution parameters based on the [3].
    SIZE_POPULATION: int = 300
    SIZE_MUTATION: int = int(SIZE_POPULATION/5)
    SIZE_CROSSOVER: int = int(SIZE_POPULATION/5)

    PROB_MUTATION: float = 0.25
    PROB_MUTATION_SELECTION: float = 1/3
    PROB_CROSSOVER : float = 1.0

    #WEIGHT_WORKFLOAD: float = 1.0700126186173278
    #WEIGHT_BALANCE: float = 3829.076062191863
    #WEIGHT_FAILURE: float = 1708.8470872135106
    #WEIGHT_NETWORK: float = 15.48341559969746

    WEIGHT_WORKFLOAD: float = 0.35
    WEIGHT_BALANCE: float = 0.15
    WEIGHT_FAILURE: float = 0.25
    WEIGHT_NETWORK: float = 0.25

    MAX_GENERATION: int = 300

    APP_REQ = [1.0, 1.5, 2.0]
    MS_MIN_SCALE = 1
    MS_MAX_SCALE = 10
    

class SocksShopConfig:
    MS_MAX_LEN = 14
    MS_NAME = ['worker', 'shipping', 'queue-master', 'payment', 'orders', 'login', 'front-end', 'edge-router', 'catalogue', 'cart', 'accounts', 'weavedb', 'rabbitmq', 'consul']
    MS_REQUEST = [3.2, 1.8, 3.2, 1.4, 2.3, 0.8, 15.1, 15.1, 12.0, 3.2, 0.1, 3.2, 3.2, 3.2]
    MS_RESOURCE = [0.1, 11.7, 20.0, 0.1, 27.1, 2.8, 3.8, 0.5, 0.2, 41.3, 45.1, 26.3, 4.0, 13.2]
    MS_THRESHOLD = [1.0, 25.0, 200.0, 10.0, 80.0, 30.0, 50.0, 10.0, 3.0, 100.0, 100.0, 80.0, 40.0, 100.0]
    MS_FAILURE = [0.04, 0.02, 0.02, 0.0002, 0.02, 0.0001, 0.003, 0.0001, 0.0006, 0.02, 0.003, 0.04, 0.0006, 0.0003]
    MS_CONSUMER = [
        set({}), set({13}), set({2, 4}), set({}), set({2,4,10,11,12}), set({}),
        set({5,6,9 }), set({7}), set({}), set({12}), set({12}), set({}), set({1,3}), set({}),
    ]
