import os
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
####################################################################################
# Part: Preprocess
####################################################################################




### transform the graph in other forms into Directed Weighted one
"""
input: path of the data file, is_weighted, is_directed
output: write aaaa file 'd_w_originalName.txt' , which can be read as aaaa directed weighted graph,

if unweighted
  --> add the 3rd col all 1
if undirected (multiple edges between 2 nodes is NOT allowed)
  if each edge twice, (aaaa,b,w) (b,aaaa,w)
      --> no need to modify --> to simplify the coding (aaaa,b,w) (b,aaaa,w) (b,aaaa,w) (aaaa,b,w)
  if each edge once, (aaaa,b,w)
      --> (aaaa,b,w),(b,aaaa,w)
"""


class Preprocessor:
    def __init__(self, logger, ):
        self.logger = logger
        self.PKL_DIR = "../eplots_1121/pkl"
        self.PKL_PREFIX = f"{self.network.did}_{int(self.network.lamb)}_{self.obj}"  # without method since attribute of subclass
        self.RESULT_LIST = ['I', 'W', 'RI', 'RW']






def transform_graph_to_weighted_directed(txt_dir, txt_name, is_weighted, is_directed):

    if is_weighted == False:
        transform_graph_to_weighted(txt_dir, txt_name)
    else:
        os.rename(txt_dir+txt_name, txt_dir+'w_'+txt_name)

    if is_directed == False:
        transform_graph_to_directed(txt_dir, 'w_'+txt_name)
    else:
        os.rename(txt_dir+'w_'+txt_name,txt_dir+'d_w_'+txt_name)


def transform_graph_to_weighted(txt_dir, txt_name):
    file1 = open(txt_dir+txt_name, "r")
    file2 = open(txt_dir+'w_'+txt_name,"w")
    while True:
        line = file1.readline()
        if not line:
            break
        line_strip = line.rstrip()
        if not len(line_strip) or line_strip.startswith('#') or line_strip.startswith('%'):
            continue
        file2.write(line_strip + " 1\n")
    file1.close()
    file2.close()

def transform_graph_to_directed(txt_dir, txt_name):
    file1 = open(txt_dir+txt_name, "r")
    file2 = open(txt_dir+'d_'+txt_name,"w")

    while True:
        line = file1.readline()
        if not line:
            break
        line_strip = line.rstrip()
        if not len(line_strip) or line_strip.startswith('#'):
            continue
        line_strip_split = line_strip.split()
        line_twin = line_strip_split[1]+" "+line_strip_split[0]+" "+line_strip_split[2]
        file2.write(line)
        file2.write(line_twin+"\n")
    file1.close()
    file2.close()


def transform_id_start_from_0(txt_dir, txt_name):
    file1 = open(txt_dir+txt_name, "r")
    file2 = open(txt_dir+'i_'+txt_name,"w")
    while True:
        line = file1.readline()
        if not line:
            break
        line_strip = line.rstrip()
        if not len(line_strip) or line_strip.startswith('#'):
            continue
        line_strip_split = line_strip.split()
        new_id_a = int(line_strip_split[0])-1
        new_id_b = int(line_strip_split[1])-1
        line_minus1 = str(new_id_a)+" "+str(new_id_b)+" "+line_strip_split[2]
        file2.write(line_minus1+"\n")
    file1.close()
    file2.close()


if __name__ == "__main__":
    ## 注意！先处理权重，再处node id start
    ### only need to excute at the first time use the dataset
    ### transform the graph in other forms into Directed Weighted one, to apply the general framework
    ### processed file renamed as 'd_w_name.txt'

    # txt_dir = "datasets_selected/"
    # txt_name = "lfr_100.txt"
    # transform_id_start_from_0(txt_dir,txt_name)

    # file1 = open(txt_dir+txt_name, "r")
    # file2 = open(txt_dir+'randw_'+txt_name,"w")
    # while True:
    #     line = file1.readline()
    #     if not line:
    #         break
    #     line_strip = line.rstrip()
    #     if not len(line_strip) or line_strip.startswith('#'):
    #         continue
    #     line_strip_split = line_strip.split()
    #     # random_weight = random.random() ##[0.0,1.0)
    #     random_weight = random.uniform(0.0001,0.5)
    #     random_weight_form = '{:.2f}'.format(random_weight)
    #     line_minus1 = line_strip_split[0]+" "+line_strip_split[1]+" "+str(random_weight_form)
    #     file2.write(line_minus1+"\n")
    # file1.close()
    # file2.close()


    # g = nx.read_edgelist(txt_dir+txt_name_edge, nodetype=int, data=(('weight',float),),create_using=nx.DiGraph())
    # print(len(g.edges()))
    # file1 = open(txt_dir+txt_name_node, "r")
    # error_node_list = []
    # while True:
    #     line = file1.readline()
    #     if not line:
    #         break
    #     line_strip = line.rstrip()
    #     if not len(line_strip) or line_strip.startswith('#'):
    #         continue
    #
    #     line_strip_split = line_strip.split()
    #     print(line_strip_split)
    #     node_id = int(line_strip_split[0])
    #     cat_pub = int(line_strip_split[1])
    #
    #     if cat_pub == 1:
    #         pub_cat_1.append(node_id)
    #     if cat_pub == 2:
    #         pub_cat_2.append(node_id)
    #     if cat_pub == 3:
    #         pub_cat_3.append(node_id)
    #
    #     cur_degree_sum = pub_degree_sum[cat_pub]
    #
    #     # new_degree_sum = cur_degree_sum + g.out_degree(node_id)
    #     # pub_degree_sum[cat_pub] = new_degree_sum
    #
    #     try:
    #         new_degree_sum = cur_degree_sum + g.out_degree(node_id)
    #         pub_degree_sum[cat_pub] = new_degree_sum
    #     except:
    #         print("----------------------------------")
    #         error_node_list.append(node_id)
    #
    # print(error_node_list)
    # print(pub_degree_sum)
    # file1.close()

    # for error_node in error_node_list:
    #     print(error_node)
    #     try:
    #         out_degree = g.out_degree(error_node)
    #         print(out_degree)
    #     except:
    #         print("no out degree")
    #     try:
    #         in_degree = g.in_degree(error_node)
    #         print(out_degree)
    #     except:
    #         print("no in degree")

    # print(len(error_node_list))
    # print(len(g.nodes))
    # # print(pub_cat_3)
    # print(pub_degree_sum[1]/len(pub_cat_1))
    # print(pub_degree_sum[2]/len(pub_cat_2))
    # print(pub_degree_sum[3]/len(pub_cat_3))

    txt_dir = "datasets_selected/"
    txt_name = "epinions.txt"

    transform_graph_to_weighted(txt_dir,txt_name)

    file1 = open(txt_dir+txt_name, "r")
    file2 = open(txt_dir+'reversed_'+txt_name,"w")
    weight_dict = {}
    weight_list = []
    loop_count = 0
    while True:
        line = file1.readline()
        if not line:
            break
        line_strip = line.rstrip()
        if not len(line_strip) or line_strip.startswith('#') or line_strip.startswith('%'):
            continue
        line_strip_split = line_strip.split()
        # print(line_strip_split)
        # print(line_strip_split[0])
        # print(line_strip_split[1])
        # if(int(line_strip_split[0])==int(line_strip_split[1])):
        #     print(line_strip_split)
        #     loop_count+=1

        # w = float(line_strip_split[2])
        # weight_list.append(w)
        # if w not in weight_dict.keys():
        #     weight_dict[w]=0
        # weight_dict[w] = weight_dict[w]+1
        # print(line_strip_split[2])
    #     # weight_list.append(int(line_strip_split[2]))
    #     # weight = int(line_strip_split[2])
    #     dif = 0.2
    #     d = '{:.2f}'.format (1-dif*(w-1))
    #
        line_d = line_strip_split[1]+" "+line_strip_split[0]+" "+line_strip_split[2]
        file2.write(line_d+"\n")
        # print(loop_count)
    file1.close()
    file2.close()
    # # print(weight_list)
    # print(weight_dict)
    # X = sorted(list(weight_dict.keys()))
    # print(X)
    # Y = []
    # for weight in X:
    #     count = weight_dict[weight]
    #     Y.append(count)
    # plt.plot(X,Y,lw=0.8)
    # plt.show()
    #
    # file1.close()
    # file2.close()
    #
    # transform_id_start_from_0(txt_dir,txt_name)










