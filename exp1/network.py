
import pickle
import networkx as nx
import random
import os
import math
import time

class Net:
    """The class of the network"""
    # DATA_FIELD = []
    dataset_dict = {
        'd1': ('residence', 217, 0.9001, 'w', 0.6, 0),
        'd2': ('blogs', 1224, 3.0001, 'uw', 1, 0),
        'd3': ('dblp', 10000, 0.7001, 'w', 0.3, 1667), #r = 1667 #rank = 4029 is nodeid = 1667 with original visibility = 14
        'd5': ('politician', 5908, 2.0001, 'uw', 1, 692),
        'd6': ('github', 37700, 2.0001, 'uw', 1, 18353),
        'd7': ('epinions', 75888, 2.0001, 'uw', 1, 33862),
    }

    def __init__(self, logger, did, seed, portion):
        self.logger = logger
        self.did = did
        self.seed = seed
        self.dname, self.dsize, self.tau, self.weighted, self.distdf, self.requester = Net.dataset_dict[did]

        self.graph = self.create_graph()
        self.load_tauVisSet()

        self.portion = portion
        self.av_list = self.random_av_list(portion)
        # print(self.av_list)
        #
        # print(len(self.sources2vismember2len[self.requester]))
        # print(len(self.graph[self.requester]))
        # print(len(self.av_list))



    def random_av_list(self, portion):
        random.seed(self.seed)
        av_list = random.sample(range(0, self.dsize), math.ceil(portion* self.dsize))
        # self.logger.info(f'Finish random available users \n \
        #                      portion={portion}, av_list={av_list}, len_av_list={len(av_list)}')
        return av_list

    def create_graph(self):
        t1 = time.process_time()
        data_path = f"../zdata/{self.dname}.txt"
        if self.weighted == 'uw':
            graph = nx.read_edgelist(data_path, nodetype=int,  create_using=nx.DiGraph()) #data=(('weight', float),),
        else:
            graph = nx.read_edgelist(data_path, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
        [graph.add_node(i) for i in range(self.dsize) if i not in graph.nodes]
        t2 = time.process_time()
        self.logger.info(f"create graph using {t2 - t1}")
        return graph

    # def load_tauVisSet(self):
    #     """ lenth 和 path 都dump 了
    #     """
    #     pklsrc = f'../zdata/{self.dname}_users2vismember2lenApath.pkl'
    #     if os.path.exists(pklsrc):
    #         self.sources2_vismembers2lenAvismembers2path = pickle.load(open(pklsrc, 'rb'))
    #     else:
    #         self.sources2_vismembers2lenAvismembers2path = dict(nx.all_pairs_dijkstra(self.graph))
    #         pickle.dump(self.sources2_vismembers2lenAvismembers2path, open(pklsrc, 'wb'))

    def load_tauVisSet(self):
        """ 只 dump 了 lenth
        """
        pklsrc = f'../zdata/{self.dname}_sources2vismember2len.pkl'
        if os.path.exists(pklsrc):
            t1 = time.process_time()
            self.sources2vismember2len = pickle.load(open(pklsrc, 'rb'))
            t2 = time.process_time()
            self.logger.info(f"load sources2vismember2len.pkl {t2 - t1}")
        else:
            t1 = time.process_time()
            self.sources2vismember2len = dict(nx.all_pairs_dijkstra_path_length(self.graph, cutoff=self.tau))
            t2 = time.process_time()
            pickle.dump(self.sources2vismember2len, open(pklsrc, 'wb'))
            t3 = time.process_time()
            self.logger.info(f"compute sources2vismember2len using {t2 - t1}")
            self.logger.info(f"dump sources2vismember2len using {t3 - t2}")


    # def load_reducedVisSet(self):
    #     # 可能不如根据 load_tauVisSet 计算快
    #     pklsrc = f'../zdata/{self.dname}_users2vismember2lenApath.pkl'
    #     if os.path.exists(pklsrc):
    #         self.sources2_vismembers2lenAvismembers2path = pickle.load(open(pklsrc, 'rb'))
    #     else:
    #         self.sources2_vismembers2lenAvismembers2path = dict(nx.all_pairs_dijkstra(self.graph))
    #         pickle.dump(self.sources2_vismembers2lenAvismembers2path, open(pklsrc, 'wb'))


    def get_distVisSet(self, root, dist):
        """ 根据所有人的tau visibe set pkl计算,reduced viible set, dist: 要小于tau
        """
        # print(self.sources2vismember2len)
        # print('root', root)
        vismembers2len = self.sources2vismember2len[root]
        if dist == self.tau:
            return vismembers2len.keys()

        setV = set()
        for vismember, len in vismembers2len.items():
            if len <= dist:
                setV.add(vismember)
        return setV




