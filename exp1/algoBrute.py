

from algo import Algo
from itertools import combinations
import math
import pickle
class AlgoBrute(Algo):
    def __init__(self, logger, net, quota_list):
        self.method = 'brute'
        Algo.__init__(self, logger, net, quota_list)
        self.quotas2optsolution = self.resultdict

    def run_dump(self):
        for quota in self.quota_list:
            optsolution = self.search_resultdict(self.quotas2optsolution, quota)
            if optsolution!= None:
                print('load', quota)
                continue
            print('compute', quota)
            setM_list = list(combinations(self.net.av_list, quota))
            setM2obj = {}
            for setM in setM_list:
                obj = self.compute_obj(setM)
                setM2obj[setM] = obj
            pklfile = open(f"{self.PKL_DIR}/detail_brute/{self.net.did}_{quota}.pkl", 'ab')
            pickle.dump(setM2obj, pklfile)
            pklfile.close()

            sorted_setM2obj = sorted(setM2obj.items(), key=lambda kv: kv[1], reverse=True)
            # is empty
            self.quotas2optsolution[quota] = sorted_setM2obj[0]

        self.dump_resultdict(self.quotas2optsolution)


