
import random
import bisect
from network import Net
class Estimator:

    def __init__(self, logger, net:Net, ssize):
        self.logger = logger
        self.net = net
        self.ssize = ssize
        # self.hash_paras = self.__generate_random_hash()  # 这个要不要放在init里面呢
        # print('init hash para:', self.hash_paras)

    def generate_sample(self, candidate, setS):
        """
        ICDE Algo 3： Generate aaaa sample of the marginal gain delta(x,S).
        :return: reward = estimated_delta
        """

        norm = 1 #!! 把reward normalize 到 90% 的reward都在[0-0.2], 会影响什么？收敛速度？ 准确率？
        hash_paras = self.__generate_random_hash()

        cnt_query_sample_list = []
        cnt_query_sample = 0

        queried_set = self.net.get_distVisSet(self.net.requester, self.net.tau)
        cnt_query_sample += len(queried_set)
        cnt_query_sample_list.append(len(queried_set))
        sketch_r = self.__get_sketch(queried_set, hash_paras)


        queried_set = self.net.get_distVisSet(candidate, self.net.tau-self.net.distdf)
        cnt_query_sample += len(queried_set)
        cnt_query_sample_list.append(len(queried_set))
        sketch_x = self.__get_sketch(queried_set, hash_paras)


        sketch_setS_list = []
        for selected in setS:
            queried_set = self.net.get_distVisSet(selected, self.net.tau-self.net.distdf)
            cnt_query_sample += len(queried_set)
            cnt_query_sample_list.append(len(queried_set))
            sketch_v = self.__get_sketch(queried_set, hash_paras)
            sketch_setS_list.append(sketch_v)


        estimated_marginal = self.estimate_delta_of_x(sketch_x, sketch_r, sketch_setS_list)
        reward = estimated_marginal / norm
        # For test:
        # true_v_multi_setminus_u = get_true_v_multi_setminus_u_cardinality(visibility_u, visibility_v_multi)

        return reward, cnt_query_sample, cnt_query_sample_list





    def __generate_random_hash(self):
        """ Map x in {0,...,self.size-1} to {0,1,...,self.size*self.size-1}, {self.size}->{self.size*self.size}
        """
        m = self.net.dsize * self.net.dsize
        p = m+1
        a = random.randint(1,p)
        b = random.randint(0,p)
        return a,b,p,m


    def __get_sketch(self, setX, hash_paras):
        """
        ICDE Algo 2: Response query with KMV sketch.
        Given the parameters of uniform hash function, compute aaaa size-ssize KMV sketch
        O(|X|*log ssize), Since bisect.insort() uses binary search
        :param X:
        :param ssize: ssize
        :param hash_paras: a,b,p,m for ((a * x + b) % p) % m
        :return: a list, normalized_sketch of X
        """
        a,b,p,m = hash_paras
        sketch = []
        for x in setX:
            val = ((a * x + b) % p) % m
            if val not in sketch:
                if len(sketch) < self.ssize:
                    bisect.insort(sketch, val)
                else:
                    bisect.insort(sketch, val)
                    sketch.pop()
        normalized_sketch = [i*1.0/(m-1) for i in sketch]
        return normalized_sketch


    def estimate_cardinality(self, sketch):
        """ Estimate |X| using sketch. Tested!
        """
        kth = sketch[-1]
        return (self.ssize - 1) / kth

    def compute_merged_sketch(self, involvedSketch_list):
        """
        Given the KMV sketches from involved visible sets, compute the KMV sketch of the union of these involved visible sets
        Can be computed by their sketched directly, no need to hash the sets union
        :param sketches:
        :param ssize:
        :return:
        """
        merge_set = set()
        for sketch in involvedSketch_list:
            merge_set = merge_set.union(set(sketch))
        merge_list = list(merge_set)
        merge_list.sort()
        merged_sketch = merge_list[0:self.ssize]
        return merged_sketch

    def estimate_delta_of_x(self, sketch_x, sketch_r, sketch_setS_list):
        """
        :param sketch_x: sketch return by arm_tried
        :param sketch_r: sketch return by requester
        :param sketch_v_multi: sketches returned by available users selected already
        :param ssize:
        :return: estimated marginal gain of x, noted as delta(x,S) in ICDE
        """
        sketch_setS_union = set()
        for sketch_v in sketch_setS_list:
            sketch_setS_union = sketch_setS_union.union(sketch_v)
        # ICDE Lemma 2
        setF = set(sketch_x).difference(sketch_r).difference(sketch_setS_union)

        involvedSketch_list = sketch_setS_list.copy()
        involvedSketch_list.append(sketch_r)
        involvedSketch_list.append(sketch_x)
        merged_sketch = self.compute_merged_sketch(involvedSketch_list)
        # ICDE Theorem 3
        estimated_delta = len(setF)/self.ssize * self.estimate_cardinality(merged_sketch)

        return estimated_delta

    




