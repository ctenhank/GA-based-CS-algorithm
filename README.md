# GA-based CS Algorithm

This page consists of CS(Container Scheduling) algorithms based on the GA(Genetic Algorithm).

## 1. Justification of why you have chosen your topic.

My research topic is related data processing system, especially focusing on stream data. In these days, these kinds of system is based on the distributed system, usually managed by container which is lightweight virtualization technology in providing cloud services due to its portability, scalability. As these container technologies are rapidly growing, the scheduling is important that set properly a subset of tasks in the distributed system that consisting inter-connected nodes to save cost-efficient operations of modern applications. The container scheduling is a component of orchestration tool such as Docker SwarmKit, Google Kubernetes, Apache Mesos, and so on.

The container scheduling algorithm can be classified as the followings:

* Mathematical Modeling
* Heuristics
* Meta-Heuristics
* Machine Learning

Each class has different characteristics in terms of quality and performance. ***The container scheduling is a NP-complete problem, so it is the most widely used method to solve optimisation problems using `meta-heuristic` approaches.*** The mathematical modeling techniques model the scheduling using Integer Linear Programming formulation. It is limited for small size problems due to the complexity of computation. Machine Learning algorithms are successful due to big data to train the model. But, these algorithms has not been explored fully for container scheduling.


## 2. What is the topic?

***Container Scheduling*** which allocate tasks in distributed system as containers.

## 3. Design decision explaining why you select:

### 1. Parameters such as the size of an initial population.


### 2. Stopping criteria.

### 3. Fitness function.

### 4. Selection operator.

### 5. Crossover operator.

### 6. Mutation operator.

### 7. Generational selection strategy.

## 4. How to run your project.

```Bash
TODO
```

## 5. How to adjust parameters.

```Bash
TODO
```

## Reference
[1] Casalicchio, Emiliano. "Container orchestration: A survey." Systems Modeling: Methodologies and Tools (2019): 221-235.  
[2] Ahmad, Imtiaz, et al. "Container scheduling techniques: A survey and assessment." Journal of King Saud University-Computer and Information Sciences (2021).  
[3] Guerrero, Carlos, Isaac Lera, and Carlos Juiz. "Genetic algorithm for multi-objective optimization of container allocation in cloud architecture." Journal of Grid Computing 16.1 (2018): 113-135.