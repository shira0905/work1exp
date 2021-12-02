
from zutil import *
import math
import networkx as nx
from network import Net
from ploter import  Ploter
def mymain():


    test_ploter()
    # test_visual_dict_result()
    # test_clean_old_pkl()


    # test_unweight()
    # test_visibility_distribution()
    # create_graph('politician')
    # visualize_pkl('../zdata/residence_sources2vismember2len.pkl')



def test_ploter():
    ploter = Ploter()
    ploter.plot_k2time()
    ploter.plot_T2time()
    ploter.plot_m2time()
    ploter.plot_dsize2time()

def test_visual_dict_result():
    diduid_list = ['d1_r0', 'd3_r1667', 'd6_r18353', 'd7_r33862']
    method_list = ['brute', 'h0', 'h1', 'h2', 'h3', 'g0', 'g1']
    headrow = ['didrid', 'method', 'ssize', 'budget', 'quota', 'setM', 'obj', 't_round', 't_accum']
    tocsv_optSolution(headrow, diduid_list, method_list)

def test_unweight():
    for did, dinfo in  Net.dataset_dict.items():
        dname = dinfo[0]
        weighted = dinfo[3]
        if weighted =='uw':
            exp= "{$NF=\"\";print}"
            command = f" awk '{exp}' ../zdata/{dname}.txt > ../zdata/{dname}2.txt"
            cmd(None, command, simulation=0)

def test_visibility_distribution():
    for did, dinfo in  Net.dataset_dict.items():
        dname = dinfo[0]
        sum = 0
        pklsrc = f'../zdata/{dname}_sources2vismember2len.pkl'
        if os.path.exists(pklsrc):
            sources2vismember2len = pickle.load(open(pklsrc, 'rb'))
            print('exist')
            for source, vismember2len in sources2vismember2len.items():
                sum += len(vismember2len.keys())
            avg = sum/len(sources2vismember2len.keys())
            print(dname, avg)


def test_create_graph(dataname):
    data_path = f"../zdata/{dataname}.txt"
    graph = nx.read_edgelist(data_path, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    # [graph.add_node(i) for i in range(self.dsize) if i not in graph.nodes]
    print(len(graph.nodes))
    print(len(graph.edges))
    return graph



def test_clean_old_pkl():
    did_list = ['d1_r0', 'd3_r1667', 'd6_r18353', 'd7_r33862']
    method_list = ['brute', 'h0', 'h1', 'h2', 'h3', 'g0', 'g1']
    clean_old_pkl(did_list, method_list)

def test_visual_dict_brute():
    did_list = ['d1']
    quota_list = [1,2]
    headrow = ['did', 'quota', 'setM', 'obj']
    tocsv_rawBrute(headrow, did_list, quota_list)



def test_nx_path_algo():
    import networkx as nx
    G = nx.path_graph(5, create_using=nx.DiGraph)

    for i,edge in enumerate(G.edges):
        print(edge)
        G[edge[0]][edge[1]]['weight'] = 2*(i+1)
    print(G.adj)
    # length, path = nx.single_source_dijkstra(G, 0, cutoff=10)
    # print(length)
    # print(path)
    d = dict(nx.all_pairs_dijkstra(G, cutoff=14))
    for n, (vismember2len, vismember2path) in d.items(): # 包含14
        print('----------', n)
        print(d[n])
        print(vismember2len, vismember2path)



if __name__ == '__main__':
    mymain()