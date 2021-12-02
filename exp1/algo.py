
import networkx as nx
import time
import pickle
import datetime
from zutil import get_latest_path
class Algo:
    def __init__(self, logger, net, quota_list):
        self.logger = logger
        self.net = net
        self.quota_list = quota_list

        self.PKL_DIR = "../eplots/pkl"
        self.TIME_DIR = "../eplots/time"
        self.PKL_PREFIX = f"{self.net.did}_r{self.net.requester}_{self.method}"  # without method since attribute of subclass
        self.resultdict = self.load_resultdict()


    def load_resultdict(self):
        """Load the latest pkl under
        """
        resultdict = {}
        pklsrc = get_latest_path(self.PKL_DIR, self.PKL_PREFIX, 'pkl')
        if pklsrc != None:
            resultdict = pickle.load(open(pklsrc, 'rb'))
        return resultdict
    def load_timedict(self):
        """Load the latest pkl under
        """
        timedict = {}
        pklsrc = get_latest_path(self.TIME_DIR, self.PKL_PREFIX, 'pkl')
        if pklsrc != None:
            timedict = pickle.load(open(pklsrc, 'rb'))
        return timedict

    def search_resultdict(self, quotas2optsolution, quota):
        if quota in quotas2optsolution:
            return  quotas2optsolution[quota]
        return None

    def dump_resultdict(self, resultdict):
        """Dump the  pkl with cur_time.
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"{self.PKL_DIR}/{self.PKL_PREFIX}_{nowTime}.pkl"
        pickle.dump(resultdict, open(result_pkl_path, 'wb'))

    def dump_timedict(self, timedict):
        """Dump the  pkl with cur_time.
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"{self.TIME_DIR}/{self.PKL_PREFIX}_{nowTime}.pkl"
        pickle.dump(timedict, open(result_pkl_path, 'wb'))

    def compute_setM(self):
        pass

    def compute_obj(self, setM):
        visset_r = self.net.get_distVisSet(self.net.requester, self.net.tau)
        result = set()
        for av in setM:
            vssset_av = self.net.get_distVisSet(av, self.net.tau-self.net.distdf)
            result = result.union(vssset_av)
        result = result.difference(visset_r)
        return len(result)


