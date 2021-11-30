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

This design is baed on the paper [3].

### 0. Chromosome Represetation

There are five elements in this problem *(you can refer the attributes for each element)* [3]. 
* *Application*, *Microservice(ms)*, *Container(cont)*, *Physical Machine(pm)*, *Network*

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

| microservice id | container id |
| - | - |
| ms1 | {3, 1} |
| ms2 | {3} |
| ms3 | {2, 3} |
| ms4 | {1,2,1,1} |
| ms5 | {1} |
| ms6 | {1,2,3} |



### 1. Parameters such as the size of an initial population.

The initial population is `100` based on some tutorials in other related libraries and applications, but it can be adjusted.

### 2. Stopping criteria.

We will stop this GA(Genetic Algorithm) when a fitness is larger than a given threshold.

- *The criteria can be added for handling some errors and infinte loops.*

### 3. Fitness function.

The fitness values is the total cost for allocating the micro-services and containers. It should be minimized.

### 4. Selection operator.

`tournament selection`.

### 5. Crossover operator.

The crossover operator is quite simple method, `single-point crossover` operator. Parent can make two children at given single index.

![Single-point_Crossover](./resources/image/single-point_crossover.png)

### 6. Mutation operator.

There are three suggested methods, `SWAP`, `SHRINK`, and `GROWTH`  in [3]. we wil use the `SWAP` mutation which shuffles the array poistions of the microservice array. 

![Swap_Mutation](./resources/image/swap_mutation.png)

### 7. Generational selection strategy.



## 4. How to run your project.

```Bash
TODO
```

## 5. How to adjust parameters.

There are basic parameters such as the following, other parameters can be added later.

* *POPULATION_SIZE*
* *MUTATION_SIZE*
* *CROSSOVER_SIZE*
* *THRESHOLD*

As default, it will be assigned as global variables.

```Bash
TODO: How to configure these will be added the next week.
```

## Reference
[1] Casalicchio, Emiliano. "Container orchestration: A survey." Systems Modeling: Methodologies and Tools (2019): 221-235.  
[2] Ahmad, Imtiaz, et al. "Container scheduling techniques: A survey and assessment." Journal of King Saud University-Computer and Information Sciences (2021).  
[3] Guerrero, Carlos, Isaac Lera, and Carlos Juiz. "Genetic algorithm for multi-objective optimization of container allocation in cloud architecture." Journal of Grid Computing 16.1 (2018): 113-135.