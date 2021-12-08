from config import Config

import numpy as np
import random as rd

class Mutation:
    FACTOR = np.random.dirichlet(np.ones(3), size=1)[0]

    def __init__(self):
        pass

    def mutate(self, ms):
        mut_fn = np.random.choice(['swap', 'shrink', 'growth'], 1, p=Mutation.FACTOR)
        if mut_fn == 'swap':
            return self.swap(ms)
        elif mut_fn == 'shrink':
            return self.shrink(ms)
        elif mut_fn == 'growth':
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
                #st, end = self._range(len(_ms))
                # check the range of shrink
                st = 1
                end = len(_ms) -1
                ret.append(rd.sample(_ms, rd.randint(st, end)))
        return ret

    def growth(self, ms):
        ret = []
        for _ms in ms:
            #st, end = self._range(len(_ms))
            num_add = rd.randint(1, 3)
            st = 0
            end = Config.CUR_NUM_PM - 1
            add = [rd.randint(st, end) for _ in range(num_add)]
            ret.append(_ms + add)
        return ret