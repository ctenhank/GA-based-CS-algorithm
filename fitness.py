from config import *

import numpy as np

# The string `Individual` in the parameter of function is for hinting type
# This is for avoiding circular import by PEP484 

def threshold_distance(ind: 'Individual'):
    thr_dist = 0.0
    for ms in ind.ms:
        thr_dist += abs(ind.cont[ms.cont_list[0]].res - SocksShopConfig.MS_THRESHOLD[ms.id])
    return thr_dist

def balanced_cluster_use(ind: 'Individual'):
    return np.std([ pm.usage for pm in ind.pm if pm.usage != 0.0 ])

def _service_failure(ind: 'Individual', ms_id: int):
    ms = ind.ms[ms_id]
    pm_allocated = set([ ind.cont[i].pm for i in ms.cont_list ])
    srv_fail = 1.0
    for i in pm_allocated:
        pm = ind.pm[i]
        cnt = pm.ms_cnt[ms_id]
        srv_fail *= (pm.FAILURE + SocksShopConfig.MS_FAILURE[ms_id] ** cnt)
    return srv_fail

# the reliability of the system
def system_failure(ind: 'Individual'):
    sys_fail = 0.0
    for i in range(SocksShopConfig.MS_MAX_LEN):
        sys_fail += _service_failure(ind, i)
    return sys_fail    

def _service_mean_distance(ind: 'Individual', ms_id: int):
    srv_mean_dist = 0.0
    ms1_pm = [i for i in ind.ms[ms_id].cont_list]

    for ms2_id in SocksShopConfig.MS_CONSUMER[ms_id]:
        ms2_pm = [i for i in ind.ms[ms2_id].cont_list]

        dist = 0
        for i in ms1_pm:
            pm1_type = ind.pm[i].rack
            for j in ms2_pm:
                pm2_type = ind.pm[j].rack

                if pm1_type == pm2_type:
                    dist += 1
                else:
                    dist += 4
        dist /= (len(ms1_pm) * len(ms2_pm))
        srv_mean_dist += dist
    return srv_mean_dist

def total_network_distance(ind: 'Individual'):
    tot_net_dist = 0.0
    for i in range(SocksShopConfig.MS_MAX_LEN):
        tot_net_dist += _service_mean_distance(ind, i)
    return tot_net_dist    

def weighted_sum(ind: 'Individual'):
    workload = Config.WEIGHT_WORKFLOAD * threshold_distance(ind)
    balance = Config.WEIGHT_BALANCE * balanced_cluster_use(ind)
    failure = Config.WEIGHT_FAILURE * system_failure(ind)
    network = Config.WEIGHT_NETWORK * total_network_distance(ind)

    return workload + balance + failure + network