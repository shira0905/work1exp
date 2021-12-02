
import math
from estimator import Estimator
class Sampler:
    """
    UCB
    """
    def __init__(self, logger, net, estimator, budget, candidate_set, normalizer, H_raw, a):
        self.logger = logger
        self.net = net
        self.estimator = estimator
        self.budget = budget

        self.candidate_set = candidate_set
        self.avs2counts = {}
        self.avs2values  ={}
        for i in candidate_set:
            self.avs2counts[i] = 0
            self.avs2values[i] = 0

        self.normalizer = normalizer
        # self.upper_a = 25 * (budget - len(candidate_set)) \
        #                / (36 * H_raw * self.net.dsize * self.net.dsize)
        # self.reduced_upper_a = 25 * (budget - len(candidate_set)) \
        #                / (36 * len(candidate_set) * self.net.dsize * self.net.dsize)
        # self.logger.info(f"a0 = {self.upper_a}; a1 = {self.reduced_upper_a}")
        # self.H_raw = H_raw
        self.a = 0.00001 # self.upper_a


    def get_optcandidate_estimated(self, setS):
        cnt_query_optcandidate = 0
        for t in range(0, len(self.candidate_set)):
            chosen_arm = list(self.candidate_set)[t]
            reward, cnt_query_sample, cnt_query_sample_list= self.estimator.generate_sample(chosen_arm, setS)
            reward = reward/self.normalizer
            self.logger.info(f"time={t}, cnt_query_sample={cnt_query_sample}, {cnt_query_sample_list}")
            cnt_query_optcandidate += cnt_query_sample
            self.update(chosen_arm, reward)
        for t in range(len(self.candidate_set), self.budget):
            chosen_arm = self.select_arm()  # arm is x in ICDE            end_time = time.time()
            reward, cnt_query_sample, cnt_query_sample_list = self.estimator.generate_sample(chosen_arm, setS)
            reward = reward / self.normalizer
            self.logger.info(f"time={t}, cnt_query_sample={cnt_query_sample}, {cnt_query_sample_list}")
            cnt_query_optcandidate += cnt_query_sample
            self.update(chosen_arm, reward)
        sorted_avs2values = sorted(self.avs2values.items(), key=lambda kv: kv[1], reverse=True)
        self.logger.info(sorted_avs2values[0:3])
        optcandidate = sorted_avs2values[0][0]
        return optcandidate, cnt_query_optcandidate

    def select_arm(self):
        avs2ucb = {}
        for i in self.candidate_set:
            avs2ucb[i] = 0.0
        total_counts = sum(self.avs2counts.values())
        for arm in self.candidate_set:
            # bonus = math.sqrt((math.log(total_counts)) / float(self.avs2counts[arm]))
            bonus = math.sqrt( self.a / float(self.avs2counts[arm]))
            avs2ucb[arm] = self.avs2values[arm] + bonus
        sorted_avs2ucb = sorted(avs2ucb.items(), key=lambda kv: kv[1], reverse=True)
        index_of_max = sorted_avs2ucb[0][0]
        return index_of_max

    def update(self, chosen_arm, reward):
        self.avs2counts[chosen_arm] = self.avs2counts[chosen_arm] + 1
        n = self.avs2counts[chosen_arm]
        value = self.avs2values[chosen_arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.avs2values[chosen_arm] = new_value
        return

