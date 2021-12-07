from typing import List, Callable
from config import *
from fitness import *
from functools import partial

import json
import argparse
import random as rd
import copy
import numpy as np
import sys
import datetime
import time

class Application:
    CNT = 0
    def __init__(self):
        self.id = Application.CNT
        self.ureq = 1.0

        Application.CNT += 1


class MicroService:
    NAME = SocksShopConfig.MS_NAME
    REQUEST = SocksShopConfig.MS_REQUEST
    RESOURCE = SocksShopConfig.MS_RESOURCE
    THRESHOLD = SocksShopConfig.MS_THRESHOLD
    FAILURE = SocksShopConfig.MS_FAILURE
    CONSUMER = SocksShopConfig.MS_CONSUME

    def __init__(self, id: int, scale: int = None):
        self.id = id
        if scale == None:
            self.scale = rd.randint(1, 10)
        else:
            self.scale = scale
        self.cont_list = []
        self.pm_list = []


class Container:
    def __init__(self, id: int, ms: MicroService):
        self.id = id
        self.type = ms.id
        self.res = self._update_resource(ms)
        # not allocated yet
        self.pm = -1

    def _update_resource(self, ms: MicroService):
        return abs((1 * ms.REQUEST[ms.id] * ms.RESOURCE[ms.id]) / ms.scale)

class PhysicalMachine:
    CNT = 0
    FAILURE = Config.PM_FAILURE

    def __init__(self):
        self.id = PhysicalMachine.CNT
        self.alloc_list = []
        self.ms_cnt = {}

        for i in range(SocksShopConfig.MS_MAX_LEN):
            self.ms_cnt[i] = 0

        self.cap_total = rd.choice(Config.PM_CAPABILITY)
        self.cap_occupied = 0.0
        self.usage = 0.0
        self.rack = rd.choice(Config.RACK_TYPE)

        PhysicalMachine.CNT += 1

    def network_distance(self, pm_rack):
        if self.rack == pm_rack:
            return 1 
        return 4

    # 13 번
    def _check_capacity(self, cont: Container):
        if (self.cap_total - self.cap_occupied) >= cont.res:
            return True
        return False

    def alloc_cont(self, cont: Container):
        """alloc_cont
        Allocate a container in this pm(Physical Machine).

        Args:
            cont (Container): [description]
        """
        if self._check_capacity(cont):
            self.alloc_list.append(cont.id)
            self.cap_occupied += cont.res
            self.usage = self.cap_occupied / self.cap_total
            if cont.type not in self.ms_cnt:
                self.ms_cnt[cont.type] = 0
            self.ms_cnt[cont.type] += 1 
            cont.pm = self.id
            return True
        return False

    def include(self, cont: Container):
        if cont.id in self.alloc_list:
            return True
        return False
        

class Mutation:
    FACTOR = np.random.dirichlet(np.ones(3), size=1)
    def __init__(self):
        pass

    def select_mutation(self, ms):
        select = np.random.choice(['swap', 'shrink', 'growth'], 1, p=Mutation.FACTOR)
        if select == 'swap':
            return self.swap(ms)
        elif select == 'shrink':
            return self.shrink(ms)
        elif select == 'growth':
            return self.growth(ms)

    def swap(self, ms):
        return rd.sample(ms, len(ms))

    def _range(self, ms_len):
        st = 1
        end = int(ms_len / 4)
        if st > end:
            t = st
            st = end
            end = t
        return st, end

    def shrink(self, ms):
        ret = []
        for _ms in ms:
            if len(_ms) == 1:
                ret.append(_ms)
            else:
                st, end = self._range(len(_ms))
                ret.append(rd.sample(_ms, rd.randint(st, end)))
        return ret

    def growth(self, ms):
        ret = []
        for _ms in ms:
            st, end = self._range(len(_ms))
            num_add = rd.randint(st, end)
            add = [rd.randint(0, Individual.PM_SIZE - 1) for _ in range(num_add)]
            ret.append(_ms + add)
        return ret

class Individual:
    INITIALIZE_CLASS = False
    DEBUG = False
    APP: Application
    # Assume that populations is calcuated on common a cluster of physical machine
    PM_SIZE: int
    PM: List[PhysicalMachine]
    FUNC_FITNESS: Callable
    THR_FITNESS: float
    MUTATION: Mutation

    def __init__(self, mul_obj= False, fn='scale', offspring=False):
        self._initialize_class(mul_obj, fn)
        self.app = copy.deepcopy(self.APP)
        self.pm = copy.deepcopy(self.PM)

        if not offspring:
            self.ms: List[MicroService] = [ MicroService(id=i) for i in range(SocksShopConfig.MS_MAX_LEN) ]
            self.cont: List[Container] = self._gen_cont_round_robin()
            # allocate the containers to pm
            self._allocate_cont()

    @classmethod
    def _initialize_class(cls, mul_obj= False, fn='scale'):
        if cls.INITIALIZE_CLASS == False:
            cls.INITIALIZE_CLASS = True
            cls.APP = Application()
            cls.PM_SIZE = rd.choice(Config.NUM_PM)
            cls.PM = [ PhysicalMachine() for _ in range(cls.PM_SIZE)] 
            cls.FUNC_FITNESS = threshold_distance
            cls.MUTATION = Mutation()

            if not mul_obj:
                if fn == 'scale':
                    cls.FUNC_FITNESS = threshold_distance
                    cls.THR_FITNESS = Config.THR_SCALABILITY
                elif fn == 'balance':
                    cls.FUNC_FITNESS = balanced_cluster_use
                    cls.THR_FITNESS = Config.THR_BALANCE
                elif fn == 'failure':
                    cls.FUNC_FITNESS = system_failure
                    cls.THR_FITNESS = Config.THR_FAILURE
                elif fn == 'network':
                    cls.FUNC_FITNESS = total_network_distance
                    cls.THR_FITNESS = Config.THR_NETWORK
            else:
                raise NotImplementedError('Not Implemented yet.')

    def offstring_update(self, ms):
        #print([len(_ms) for _ms in ms])
        self.ms: List[MicroService] = [ MicroService(id=i, scale=len(ms[i])) for i in range(SocksShopConfig.MS_MAX_LEN) ]
        self.cont: List[Container] = self._gen_cont_round_robin()
        # allocate the containers to the specified pm
        for i, pm in enumerate(ms):
            cont_list = self.ms[i].cont_list
            for j in range(len(pm)):
                cont_idx = cont_list[j]
                pm_idx = pm[j]
                # the resource of pm is exceeded
                while not self.pm[pm_idx].alloc_cont(self.cont[cont_idx]):
                    pm_idx = rd.randint(0, self.PM_SIZE - 1)
                self.ms[i].pm_list.append(pm_idx)

    def _allocate_cont(self):
        for cont in self.cont:
            while True:
                i = rd.randint(0, self.PM_SIZE - 1)
                if self.pm[i].alloc_cont(cont):
                    self.ms[cont.type].pm_list.append(i)
                    break

    def _gen_cont_round_robin(self):
        # something is wrong
        # this is not round robin, just sequence
        max_scale = max([ ms.scale for ms in self.ms ])
        ret = []
        len_ms = len(self.ms)
        cnt_cont = [ 0 for ms in range(len_ms) ]
        cnt = 0
        for i in range(len_ms):
            for _ in range(max_scale):
                ms = self.ms[i]
                if cnt_cont[i] > ms.scale:
                    continue 
                cnt_cont[i] += 1
                cont = Container(id=cnt, ms=ms)
                ret.append(cont)
                ms.cont_list.append(cont.id)
                cnt += 1
        return ret
    
    def debug(self):
        """[summary]
        check whether every app and pm is same in the all individual
        """
        print(f'APP:{json.dumps(self.APP.__dict__)}')
        print(f'The length of pm is {len(self.PM)}')
        for idx in range(0, 10):
            print(f'PM({idx}): {self.pm[idx].__dict__}')

        for idx in range(len(self.ms)):
            id = self.ms[idx].id
            print(f'MS({id}): {self.ms[idx].__dict__}: {MicroService.NAME[id]}, {MicroService.REQUEST[id]}, {MicroService.RESOURCE[id]}, ...')

        for i in range(len(self.ms)):
            for j in self.ms[i].cont_list:
                print(f'Cont of MS({i}): {self.cont[j].__dict__}')


class FitnessProportionalSelection:
    def __init__(self, population: List[Individual], fitness):
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



def main():
    #GMT = datetime.timezone(datetime.timedelta(hours=9))
    #start = datetime.datetime.now(tz=GMT)
    start = time.time()
    num_gen = 0
    pop = [ Individual(fn=args.fitness) for _ in range(Config.SIZE_POPULATION) ]
    best_so_far = sys.maxsize
    initial = True
    
    while True:
        #print(f'Generation: {nGen}')
        improved = False
        num_gen += 1
        scores = []
        d_scores = {}
        
        for i in range(Config.SIZE_POPULATION):
            score = Individual.FUNC_FITNESS(pop[i])
            scores.append(score)
            d_scores[i] = score

            if best_so_far > score:
                improved = True
                best_so_far = score

        if improved or initial:
            initial = False
            time_diff = time.time() - start
            print('='*50)
            print(f'Generation: {num_gen}')
            print(f'Elapsed Time: {time_diff}')
            print(f'Best-so-far: {best_so_far}')
            print('='*50)

            if best_so_far <= Individual.THR_FITNESS or num_gen > Config.MAX_GENERATION:
                print('Finished')
                break

        next_pop = []
        next_pop2 = copy.deepcopy(pop)
        fps = FitnessProportionalSelection(pop, scores)
        # crossover
        for _ in range(Config.SIZE_CROSSOVER):
            a, b = fps.select()
            off1 = []
            off2 = []
            cnt_no_change = 0
            for i in range(SocksShopConfig.MS_MAX_LEN):
                range_ = min(a.ms[i].scale, b.ms[i].scale)
                point = rd.randint(0, range_ - 1)

                # single-point crossover
                off1.append(a.ms[i].pm_list[:point+1] + b.ms[i].pm_list[point+1:])
                off2.append(b.ms[i].pm_list[:point+1] + a.ms[i].pm_list[point+1:])

                if point == range_ - 1:
                    cnt_no_change += 1

            # Duplicated case
            if cnt_no_change == SocksShopConfig.MS_MAX_LEN:
                continue
            
            offspring1 = Individual(offspring=True)
            offspring2 = Individual(offspring=True)
            offspring1.offstring_update(off1)
            offspring2.offstring_update(off2)

            #next_pop.append(offspring1)
            #next_pop.append(offspring2)

            next_pop2.append(offspring1)
            next_pop2.append(offspring2)

        # mutation
        for _ in range(Config.SIZE_MUTATION):
            i = rd.randint(0, len(next_pop2))
            ms = copy.deepcopy(next_pop2[i].ms)
            new_ms = Individual.MUTATION.select_mutation(ms)
            mutant = Individual(offspring=True)
            mutant.offstring_update(new_ms)
            #next_pop.append(mutant)
            next_pop2.append(mutant)            

        # sorting
        for i in range(Config.SIZE_POPULATION, len(next_pop2)):
            score = Individual.FUNC_FITNESS(next_pop2[i])
            d_scores[i] = score

        pop += next_pop
        best = sorted(d_scores.items(), key = lambda item: item[1])[:Config.SIZE_POPULATION]

        #sorted(d.items(), key = lambda item: item[1])[:Config.SIZE_POPULATION]
        next_pop = []
        for i in best:
            next_pop.append(next_pop2[i[0]])
        pop = next_pop

        



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--fitness', default='scale', help='must be one of the ["scale", "balance", "failure", "network"]')
    args = parser.parse_args()

    main()



    