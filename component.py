from typing import List, Callable
from mutation import Mutation
from config import *
import random as rd
from copy import deepcopy
from fitness import (threshold_distance, total_network_distance, system_failure, balanced_cluster_use)


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
    CONSUMER = SocksShopConfig.MS_CONSUMER

    def __init__(self, id: int, scale: int = None):
        self.id = id
        if scale == None:
            self.scale = rd.randint(Config.MS_MIN_SCALE, Config.MS_MAX_SCALE)
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

    def __init__(self, mul_obj= False, fn='scale', derived=False):
        self._initialize_class(mul_obj, fn)
        self.app = deepcopy(self.APP)
        self.pm = deepcopy(self.PM)

        if not derived:
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
            Config.CUR_NUM_PM = cls.PM_SIZE

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