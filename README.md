# GA-based CS Algorithm

This page consists of CS(Container Scheduling) algorithms based on the GA(Genetic Algorithm).

## 1. Justification of why you have chosen your topic.

My research topic is related data processing system, especially focusing on stream data. These days, the modern data processing system is based on the distributed system to process big, big, and big data. The most popular and common-used technology is the container which is a lightweight virtualization in providing cloud services. It provides portability, scalability, and flexible deployment. As the usage of these container technologies are rapidly growing, the scheduling is important that set properly an application as a subset of tasks in the distributed system, that consisting inter-connected nodes, to save cost-efficient operations of modern applications. So, it is one of core components in orchestration tool such as Docker SwarmKit, Google Kubernetes, Apache Mesos, and so on.

The container scheduling algorithms can be classified as the followings:

* Mathematical Modeling
* Heuristics
* Meta-Heuristics
* Machine Learning

Each class has different characteristics in terms of quality and performance. ***The container scheduling is a NP-complete problem, so it's the most widely used method to solve optimisation problems using `meta-heuristic` approaches***. The mathematical modeling techniques model the scheduling using Integer Linear Programming formulation, but it's limited for small size problems due to the complexity of computation. And, Machine Learning algorithms are successful because of big data to train the model. But, these algorithms has not been explored fully for container scheduling.

## 2. What is the topic?

***Container Scheduling*** which allocate tasks in distributed system as containers.

## 3. Design decision explaining why you select:

This design is based on the paper [3].

### 0. Chromosome Represetation

There are five elements in this problem *(you can refer the attributes for each element)*[3].  
*The string in brackets means an abbreviation of the full string.* 

*It's represented as an image due to unsupporting inline latex in Github. You can check the original text in `backup/README.md.bk` directory and get more clear image when you left-click this image.* 

![Elements](./resources/image/elements.png)

We need to set some fixed applications and corresponding micro-services. 

**Example**

Abbreviations: *Microservice(ms)*, *Container(cont)*, *Physical Machine(pm)*

*pm1*
| cont1 | cont2 | cont3 | cont4 | cont5 | cont6|
|-|-|-|-|-|-|
| ms4 | ms1 | ms5 | ms4 | ms6 | ms4 |

*pm2*
| cont7 | cont8 | cont9 |
|-|-|-|
| ms3 | ms4 | ms5 |

*pm3*
| cont10 | cont11 | cont12 | cont13 |
|-|-|-|-|
| ms1 | ms2 | ms6 | ms3 |

The chromosome represetation of the above example is the following:

| microservice id | Physical Machine id |
| - | - |
| ms1 | {3, 1} |
| ms2 | {3} |
| ms3 | {2, 3} |
| ms4 | {1,2,1,1} |
| ms5 | {1} |
| ms6 | {1,2,3} |

### 1. Parameters such as the size of an initial population.

There are two type parameters: `basic parameters`, `application-specific parameters`. The `basic parameters` are genetic-algorithm parameters such as the size of population, crossover, mutation and the thresholds to finish the program. 

**Basic Parameters**

* *POPULATION_SIZE=300*
* *CROSSOVER_SIZE=POPULATION_SIZE/5*
* *MUTATION_SIZE=POPULATION_SIZE/5*
* MS_MIN_SCALE = 1
* MS_MAX_SCALE = 10
* APP_REQ = [1.0, 1.5, 2.0]

**Application-Specific Parameters**

The application-specific parameters are metrics for each micro-services. In this scripts, we only consider the use case *Sock Shop*[4], one of the most popular demo in cloud system. The specific metric is giveb in [3].

* MS_MAX_LEN = 14
* MS_NAME = ['worker', 'shipping', 'queue-master', 'payment', 'orders', 'login', 'front-end', 'edge-router', 'catalogue', 'cart', 'accounts', 'weavedb', 'rabbitmq', 'consul']
* MS_REQUEST = [3.2, 1.8, 3.2, 1.4, 2.3, 0.8, 15.1, 15.1, 12.0, 3.2, 0.1, 3.2, 3.2, 3.2]
* MS_RESOURCE = [0.1, 11.7, 20.0, 0.1, 27.1, 2.8, 3.8, 0.5, 0.2, 41.3, 45.1, 26.3, 4.0, 13.2]
* MS_THRESHOLD = [1.0, 25.0, 200.0, 10.0, 80.0, 30.0, 50.0, 10.0, 3.0, 100.0, 100.0, 80.0, 40.0, 100.0]
* MS_FAILURE = [0.04, 0.02, 0.02, 0.0002, 0.02, 0.0001, 0.003, 0.0001, 0.0006, 0.02, 0.003, 0.04, 0.0006, 0.0003]
* MS_CONSUMER = [
    {}, {13}, {2, 4}, {}, {2,4,10,11,12}, {}, {5,6,9}, {7}, {}, {12}, {12}, {}, {1,3}, {},
]


### 2. Stopping criteria.

This algorithm will stop whether when the best-so-far is smaller than a given threshold or the step of algorithm exceeds the given `MAX_GENERATION`. The default configurations are below.

* MAX_GENERATION = 300


### 3. Fitness function.

***Weighted Sum*** of the following fitness values:
* Thresholod Distance
* Balanced Cluster Usage
* System Failure
* Total Network Distance

The weight is following
* WEIGHT_WORKFLOAD: float = 0.35
* WEIGHT_BALANCE: float = 0.15
* WEIGHT_FAILURE: float = 0.25
* WEIGHT_NETWORK: float = 0.25

*It's represented as an image due to unsupporting inline latex in Github. You can check the original text in `backup/README.md.bk` directory and get more clear image when you left-click this image.*
##### ![Fitness Function](./resources/image/fitness.png)

### 4. Selection operator.

`Fitness Proportional Selection`.

### 5. Crossover operator.

The crossover operator is quite simple method, `single-point crossover` operator. Parent can make two children at given single index.

##### ![Single-point_Crossover](./resources/image/single-point_crossover.png)

### 6. Mutation operator.

This application supports randomly three swap functions for each mutation: `SWAP`, `SHRINK`, and `GROWTH`.

![Mutations](./resources/image/mutation.png)

### 7. Generational selection strategy.

`Elitism`

## 4. How to run your project.

### Installation
```Bash
git clone https://github.com/ctenhank/GA-based-CS-algorithm

# Recommend the usage of virtual environments
python3 -m venv venv
source venv/bin/activate

# (venv)
pip3 install -r requirements.txt

```

### Execution
```bash
python3 app.py
```

There are some options to execute this application, the container scheduling using meta-heuristice algorithm. One of the options is to select a fitness function to evaluate population.
```bash
# Select one of fitness function in ['scale', 'balance', 'failure', 'network']
# The fastest result is `balance` means the balanced cluster usage.
python3 app.py --fitness {OPTION_FITNESS}
```

## 5. How to adjust parameters.

You can configure the parameters in the `config.py`

## Reference
[1] Casalicchio, Emiliano. "Container orchestration: A survey." Systems Modeling: Methodologies and Tools (2019): 221-235.  
[2] Ahmad, Imtiaz, et al. "Container scheduling techniques: A survey and assessment." Journal of King Saud University-Computer and Information Sciences (2021).  
[3] Guerrero, Carlos, Isaac Lera, and Carlos Juiz. "Genetic algorithm for multi-objective optimization of container allocation in cloud architecture." Journal of Grid Computing 16.1 (2018): 113-135.
[4] "Sock Shop", https://microservices-demo.github.io/, accessed on 2021-12-08