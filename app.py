from config import *
from component import Individual
from selection import *

import sys
import copy
import time
import argparse
import random as rd
    
def main():
    #GMT = datetime.timezone(datetime.timedelta(hours=9))
    #start = datetime.datetime.now(tz=GMT)

    # Initialization
    num_gen = 0
    start = time.time()
    pop = [ Individual(fn=args.fitness) for _ in range(Config.SIZE_POPULATION) ]
    best_so_far = sys.maxsize
    initial = True
    
    while True:
        improved = False
        num_gen += 1
        scores = []
        d_scores = {}
        
        # Part1: Generate the fitness values
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

        # Stopping criteria
        if best_so_far <= Individual.THR_FITNESS or num_gen > Config.MAX_GENERATION:
                print('Finished')
                break

        # Part2: Crossover
        next_pop = copy.deepcopy(pop)
        fps = FitnessProportionalSelection(pop, scores)
            
        for _ in range(Config.SIZE_CROSSOVER):
            # part2-1: selection
            a, b = fps.select()

            # part2-2: single-point crossover
            off1 = []
            off2 = []
            cnt_no_change = 0
            for i in range(SocksShopConfig.MS_MAX_LEN):
                range_ = min(a.ms[i].scale, b.ms[i].scale)
                point = rd.randint(0, range_ - 1)

                off1.append(a.ms[i].pm_list[:point+1] + b.ms[i].pm_list[point+1:])
                off2.append(b.ms[i].pm_list[:point+1] + a.ms[i].pm_list[point+1:])

                if point == range_ - 1:
                    cnt_no_change += 1

            # part2-3: Remove duplicated case
            if cnt_no_change == SocksShopConfig.MS_MAX_LEN:
                continue
            
            # part2-4: create new individual and update

            # This part is most time-consuming part.
            offspring1 = Individual(derived=True)
            offspring2 = Individual(derived=True)
            offspring1.offstring_update(off1)
            offspring2.offstring_update(off2)

            # part2-5: update the next population
            next_pop.append(offspring1)
            next_pop.append(offspring2)

        
        # Part3: Mutation
        for _ in range(Config.SIZE_MUTATION):
            i = rd.randint(0, len(next_pop) - 1)
            ms = [ _ms.cont_list for _ms in next_pop[i].ms ]
            # There are three type funtions: Swap, Shrink, Growth.
            # The mutation function is randomly selected.
            new_ms = Individual.MUTATION.mutate(ms)
            mutant = Individual(derived=True)
            mutant.offstring_update(new_ms)
            next_pop.append(mutant)   


        # Part4: Sorting
        for i in range(Config.SIZE_POPULATION, len(next_pop)):
            score = Individual.FUNC_FITNESS(next_pop[i])
            d_scores[i] = score

        best = sorted(d_scores.items(), key = lambda item: item[1])[:Config.SIZE_POPULATION]

        pop = []
        for i in best:
            pop.append(next_pop[i[0]])

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--fitness', default='scale', help='It must be one of the ["scale", "balance", "failure", "network"]. The default is `scale`')
    args = parser.parse_args()

    main()