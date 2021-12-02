
from estimator import Estimator
from sampler import  Sampler
from algo import Algo
import pickle
import datetime
import time
class AlgoGreedy(Algo):
    greedy_list = ['greedy_estimate', 'greedy_exact']
    def __init__(self, logger, net ,quota_list, method_g, ssize_list, budget_list, a):

        self.cnt_query = 0
        self.method = method_g
        self.greedy = AlgoGreedy.greedy_list[int(method_g[-1])]
        Algo.__init__(self, logger, net, quota_list)

        if self.greedy == 'greedy_estimate':
            self.ssize_list = ssize_list
            self.budget_list = [coef * net.dsize for coef in budget_list]
            self.ssizes2budgets2quotas2optsolution = self.resultdict
            self.a = a
            # self.ssizes2budgets2quotas2time = self.load_timedict()

        elif self.greedy == 'greedy_exact':
            self.quotas2optsolution = self.resultdict
            # self.quotas2time = self.load_timedict()



    def run_dump_g0(self):
        for ssize in self.ssize_list:
            estimator = Estimator(self.logger, self.net, ssize)
            if ssize not in self.ssizes2budgets2quotas2optsolution.keys(): # 如果pkl里面已经有了, 这个quota的, 那就不需要跑了
                self.ssizes2budgets2quotas2optsolution[ssize] = {}
            # if ssize not in self.ssizes2budgets2quotas2time.keys():self.ssizes2budgets2quotas2time[ssize] = {}
            for budget in self.budget_list:
                if budget not in self.ssizes2budgets2quotas2optsolution[ssize].keys():  # 如果pkl里面已经有了, 这个quota的, 那就不需要跑了
                    self.ssizes2budgets2quotas2optsolution[ssize][budget] = {}
                quotas2optsolution = self.run_dump_core(estimator, budget)
                self.ssizes2budgets2quotas2optsolution[ssize][budget] = quotas2optsolution # 如果已经有了的话, 是替换掉原来k t下面的所有m的用时和结果, 不合理啊, 至少quota不应该
                # self.ssizes2budgets2quotas2time[ssize][budget] = quotas2time
                self.dump_resultdict(self.ssizes2budgets2quotas2optsolution) # 每一个ssize跑完之后就记录一下
            # self.dump_timedict(self.ssizes2budgets2quotas2time)


    def run_dump_core(self, estimator, budget):
        quotas2optsolution = {}
        # quotas2time = {}
        quota_max = max(self.quota_list)
        # setM = set()
        setM = []
        cnt_query_trial = 0
        for quota in range(1, quota_max + 1):
            self.logger.info(f"=== k={estimator.ssize}, T={budget}, m={quota}, setM={setM}")
            if quota in  self.ssizes2budgets2quotas2optsolution[estimator.ssize][budget].keys():
                quotas2optsolution[quota] = self.ssizes2budgets2quotas2optsolution[estimator.ssize][budget][quota]
                setM = list(quotas2optsolution[quota][0])
                self.logger.info(f"load k={estimator.ssize}, T={budget}, m={quota}, setM={setM},")
                continue
            t1 = time.perf_counter()
            t3 = time.process_time()
            candidate_set = set(self.net.av_list).difference(set(setM)).difference(self.net.graph[self.net.requester])
            optcandidate, optmarginal, H_raw = self.get_optcandidate_exact(setM, candidate_set)
            self.logger.info(f"optcandidate={optcandidate}; optmarginal={optmarginal}; H_raw={H_raw}")
            sampler = Sampler(self.logger, self.net, estimator, budget, candidate_set, optmarginal, H_raw, self.a )
            optcandidate, cnt_query_optcandidate = sampler.get_optcandidate_estimated(setM)
            self.logger.info(f"quota={quota}, cnt_query_optcandidate={cnt_query_optcandidate}")
            cnt_query_trial += cnt_query_optcandidate
            sampler.candidate_set.remove(optcandidate)

            setM.append(optcandidate)
            obj = self.compute_obj(setM)

            t2 = time.perf_counter()
            t4 = time.process_time()
            quotas2optsolution[quota] = (setM.copy(), obj, t4-t3)
            # quotas2time[quota] = t4-t3
            self.logger.info(f"compute k={sampler.estimator.ssize}, T={sampler.budget}, m={quota}, setM={setM}, x*={optcandidate}, t_proc={t4-t3}, t_all={t2-t1}")

        return quotas2optsolution

    def run_dump_g1(self):
        quota_max = max(self.quota_list)
        setM = []
        for quota in range(1, quota_max+1):
            t1 = time.process_time()
            candidate_set = set(self.net.av_list).difference(set(setM)).difference(self.net.graph[self.net.requester])
            optcandidate, optmarginal, H_raw = self.get_optcandidate_exact(setM, candidate_set)
            setM.append(optcandidate)
            t2 = time.process_time()
            obj = self.compute_obj(setM)
            self.quotas2optsolution[quota ] = (setM.copy(), obj, t2 - t1)
        self.dump_resultdict(self.quotas2optsolution)



    def get_optcandidate_exact(self, setS, candidate_set):

        visset_r = self.net.get_distVisSet(self.net.requester, self.net.tau)
        candidate2marginal = {}
        reducedVisSet_union = set()
        for selected in setS:
            reducedVisSet_union = reducedVisSet_union.union(self.net.get_distVisSet(selected, self.net.tau-self.net.distdf))

        for x in candidate_set:
            # delta is the marginal increase if adding x given S have been chosen
            marginal = len(set(self.net.get_distVisSet(x, self.net.tau-self.net.distdf)).difference(reducedVisSet_union).difference(visset_r))
            candidate2marginal[x] = marginal
        # print(len(visset_r), len(reducedVisSet_union))
        sorted_candidate2marginal = sorted(candidate2marginal.items(), key=lambda kv: kv[1], reverse=True)
        # print(sorted_candidate2marginal[:5])
        optcandidate, optmarginal = sorted_candidate2marginal[0]

        H_raw = 0
        # for x in candidate_set:
        #     marginal = candidate2marginal[x]
        #     if x == optcandidate:
        #         marginal = sorted_candidate2marginal[1][0]
        #     H_raw += 1/ ((optmarginal - marginal)^2)
        return optcandidate, optmarginal, H_raw





    # def run_dump_g0(self):
    #     for ssize in self.ssize_list:
    #         estimator = Estimator(self.logger, self.net, ssize)
    #         budgets2quotas2optsolution = {}
    #         if ssize in self.ssizes2budgets2quotas2optsolution:
    #             budgets2quotas2optsolution = self.ssizes2budgets2quotas2optsolution[ssize]
    #
    #         for budget in self.budget_list:
    #             sampler = Sampler(self.logger, self.net, estimator, budget)
    #             quotas2optsolution = {}
    #             if budget in budgets2quotas2optsolution:
    #                 quotas2optsolution = budgets2quotas2optsolution[
    #                     budget]  # better not self., but for the api of search history
    #             max_history_quota, max_history_optsolution = 0, (set(), 0)
    #             quota_max = max(self.quota_list)
    #             for quota in range(quota_max, 0, -1):
    #                 optsolution = self.search_resultdict(quotas2optsolution, quota)
    #                 if optsolution != None:
    #                     max_history_quota, max_history_optsolution = quota, optsolution
    #                     break
    #             setM_last = set()
    #             if max_history_quota > 0:
    #                 setM_last = max_history_optsolution[0]
    #             for quota_last in range(max_history_quota, quota_max):
    #                 optcandidate = sampler.get_optcandidate_estimated(setM_last)
    #
    #                 setM_last.add(optcandidate)
    #                 obj = self.compute_obj(setM_last)
    #                 # 相比返回list, 是不是可以吧opt_set直接接口到get_marginal_greedy
    #                 quotas2optsolution[quota_last + 1] = (setM_last.copy(), obj)
    #             budgets2quotas2optsolution[budget] = quotas2optsolution
    #         self.ssizes2budgets2quotas2optsolution[ssize] = budgets2quotas2optsolution
    #     print(self.ssizes2budgets2quotas2optsolution)
    #     self.dump_resultdict(self.ssizes2budgets2quotas2optsolution)

    # def run_dump_g1(self):
    #     max_history_quota, max_history_optsolution = 0, (set(), 0)
    #     quota_max = max(self.quota_list)
    #     for quota in range(quota_max, 0, -1):
    #         optsolution = self.search_resultdict(self.quotas2optsolution, quota)
    #         if optsolution != None:
    #             max_history_quota, max_history_optsolution = quota, optsolution
    #             break
    #     setM_last = max_history_optsolution[0]
    #     for quota_last in range(max_history_quota, quota_max):
    #         optcandidate = self.get_optcandidate_exact(setM_last)
    #         setM_last.add(optcandidate)
    #         obj = self.compute_obj(setM_last)
    #         self.quotas2optsolution[quota_last + 1] = (setM_last.copy(), obj)
    #     self.dump_resultdict()



