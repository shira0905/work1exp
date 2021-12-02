

from algo import Algo
import networkx as nx
class AlgoHeuristic(Algo):
    centrality_list = ['in-degree', 'closeness', 'betweenness', 'PageRank']
    def __init__(self, logger, net, quota_list, method_h):
        self.centrality = AlgoHeuristic.centrality_list[int(method_h[-1])]
        self.method = method_h
        Algo.__init__(self, logger, net, quota_list)
        self.quotas2optsolution = self.resultdict

    def run_dump(self):
        for quota in self.quota_list:
            optsolution = self.search_resultdict(self.resultdict, quota)
            if optsolution!= None:
                print('load', quota)
                continue
            print('compute', quota)
            setM = self.get_topM_centrality(quota, self.centrality)
            obj =  self.compute_obj(setM)
            self.quotas2optsolution[quota] = (setM, obj)
        self.dump_resultdict(self.quotas2optsolution)

    def get_topM_centrality(self, m, centrality):
        users2centrality = {}
        if centrality == 'in-degree':
            users2centrality = nx.out_degree_centrality(self.net.graph)
        if centrality == 'closeness':
            users2centrality = nx.closeness_centrality(self.net.graph)
        if centrality == 'betweenness':
            users2centrality = nx.betweenness_centrality(self.net.graph)
        if centrality == 'PageRank':
            users2centrality = nx.pagerank(self.net.graph, alpha=0.85)
        sorted_users2centrality = sorted(users2centrality.items(), key=lambda kv: kv[1], reverse=True)

        setM = []
        for item in sorted_users2centrality:
            if item[0] not in self.net.graph[self.net.requester]:
                setM.append(item[0])
            if len(setM) == m:
                break
        return setM

