from abc import abstractmethod
from typing import List
import random as rd

class BaseSelection:
    def __init__(self):
        pass

    @abstractmethod
    def select(self):
        raise NotImplementedError('You must implement this function')

class FitnessProportionalSelection(BaseSelection):
    def __init__(self, population: List, fitness):
        self.__population = population
        self.__fitness = fitness
        self.__probability_for_each_fitness = self._get_probability_for_each_fitness(
            self.__fitness,
            self._sum_fitness(self.__fitness)
        )

    def _sum_fitness(self, fitness):
        sum = 0
        for afitness in fitness:
            sum += afitness
        return sum

    def _get_probability_for_each_fitness(self, fitness, summation):
        ret = []
        for idx in range(len(fitness)):
            ret.append(fitness[idx] / summation)
        return ret

    def select(self):
        return rd.choices(
            population=self.__population,
            weights=self.__probability_for_each_fitness,
            k=2)