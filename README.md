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

* Application($app_j$): Each $app_j$ consists of the stack of micro-services in the cloud architecture. 
    * User Request($ureq_j$): User Request

* Micro-service($ms_i$): A series of micro-services($ms_i$) constitute an application, each of which performs a function.
    * $(ms_{i'}, ms_i)_{prod/cons}$: An application consists of the stack of microservices that means the interoperability of the microservices. It can be modeled as a directed graph.
    * Micro-service Request($msreq_i$): Required ms-request to meet on an $ureq_j$ of one *app*
    * Resource($res_i$): Required computational resources to process one $msreq_i$
    * Threshold($thr_i$): Threshold level for the consumption of resources. if it's above $thr_i$, the service performance will be downgraded and ms will produce a bottlement for the $app_j$
    * Failure($fail_i$): Failure rate of the $ms_i$
    * Scale($scale_i$): The scale level of ms mean that the number of containers to execute this $ms_i$.
    
    
* Container($cont_k$): one or more containers $cont_k$ are encapsulated and executed for each ms($ms_i$)
    * Type: The $ms_i$ type of container, represented as $ms_i \equiv cont_k$
    * Resource($res_k$): The computational resources consumption of the container $res_k$, calculated as $\frac {ureq_j \times msreq_i \times res_i}{scale_i}$

* Physical Machine($pm_l$): executes a set of containers
    * $alloc(ms_i/cont_k) = pm_l$: Container $cont_k$ is allocated to the $pm_l$
    * Capability($cap_l$) : The computational capability
    * Failure($fail_l$) : Failure rate of the $pm_l$
    

* Network
    * $dist_{pm_l, pm_{l'}}$ : The paths between nodes $pm_l$, $pm_{l'}$


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

The initial population is `200` based on some tutorials in other related libraries and applications, but it can be adjusted.

**Parameters for genetic algorithm**

* *POPULATION_SIZE=200*
* *CROSSOVER_SIZE=POPULATION_SIZE/2*
* *MUTATION_SIZE=POPULATION_SIZE/10*

**Parameters for element**

* *MAX_LENGTH_APPLICATIONS=1*
* *MAX_LENGTH_PHYSICAL_MACHINE=300*
* *MAX_LENGTH_MICROSERVICES=14*
* *MAX_LENGTH_CONTAINER=20*

**Parameters for stopping criteria**

* *STOP_MAX_INTERVAL_SOLUTIONS=10*
* *STOP_MAX_GENERATION=300*
* *STOP_THRESHOLD={NOT-DETERMINED}*


### 2. Stopping criteria.

We will stop this GA(Genetic Algorithm) when a fitness is larger than a given threshold. There are three options as following:

1. The maximum interval of solutions, which is no change in the given value as the parameter `STOP_MAX_INTERVAL_SOLUTIONS`(default: 10)
2. The fixed number of generations as the parameter `STOP_MAX_GENERATION`(default: 300)
3. The fitness value exceeds a given threshold as the parameter `STOP_THRESHOLD`(default: *{NOT YET}*)

*The criteria can be added for handling some errors and infinte loops.*

### 3. Fitness function.

The fitness values is the total cost for allocating the micro-services and containers. It should be minimized.

***Determine***

$scale_i = |\{cont_k\}|\ cont_k \equiv ms_i\ and\ alloc(ms_i),\ \forall_{ms_i} $ 

***by minimizing***

1. **Theshold Distance** = $\sum_{\forall_{ms_i}}|\frac{msreq_i\times res_i}{scale_i} - thr_i|$
2. **Balanced Cluster Usage** = $\sigma(PM_{usage}^{pm_l},\ if\ \exists ms_i\ |\ alloc(ms_i) = pm_l)$
    * $PM_{usage}^{pm_l}=\frac{\sum_{ms_i}res_k}{cap_l}, \forall{ms_i}\ |\ alloc(ms_i)=pm_l$
    * $res_k=\frac {ureq_j \times msreq_i \times res_i}{scale_i}$
3. **System Failure** = $\displaystyle\sum_{\forall{ms_i}}Service\ Failure(ms_i)$
    * $Service\ Failure(ms_i)=\displaystyle\prod_{\forall pm_l | alloc(ms_i)=pm_l}(fail_l +\displaystyle\prod_{\forall pm_l | alloc(ms_i)=pm_l}fail_i)$
4. **Total Network Distance** = $\displaystyle\sum_{\forall{ms_i}}Service\ Mean\ Distance(ms_i)$
    * $Service\ Mean\ Distance(ms_i) = \frac{\sum_{\forall{cont_k|cont_k\equiv ms_i}}(\sum_{\forall {cont_{k'}\equiv ms_{i'}|(ms_i, ms_{i'})_{prov/cons}}}dist_{pm_l,pm_{l'}})}{|cont_k|\times|cont_{k'}|}$

***Subject to***

$\displaystyle\sum_{\forall{cont_k}|alloc(cont_k)=pm_l}res_k<cap_l, \ \forall pm_l$


### 4. Selection operator.

`Tournament Selection`.

### 5. Crossover operator.

The crossover operator is quite simple method, `single-point crossover` operator. Parent can make two children at given single index.

![Single-point_Crossover](./resources/image/single-point_crossover.png)

### 6. Mutation operator.

There are three suggested methods, `SWAP`, `SHRINK`, and `GROWTH`  in [3]. we wil use the `SWAP` mutation which shuffles the array poistions of the microservice array. 

![Swap_Mutation](./resources/image/swap_mutation.png)

### 7. Generational selection strategy.

`Elitism`

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
* *MAX_INTERVAL_SOLUTIONS*

As default, it will be assigned as global variables.

```Bash
TODO: How to configure these will be added the next week.
```

## Point-out

* No specific value in the parameter, stopping criteria.
* No specific fiteness values
    * Equations
    * Metrics
* More clear explainataion
* Can we merge ms and cont just as ms?


## Reference
[1] Casalicchio, Emiliano. "Container orchestration: A survey." Systems Modeling: Methodologies and Tools (2019): 221-235.  
[2] Ahmad, Imtiaz, et al. "Container scheduling techniques: A survey and assessment." Journal of King Saud University-Computer and Information Sciences (2021).  
[3] Guerrero, Carlos, Isaac Lera, and Carlos Juiz. "Genetic algorithm for multi-objective optimization of container allocation in cloud architecture." Journal of Grid Computing 16.1 (2018): 113-135.