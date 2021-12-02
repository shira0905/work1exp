#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/11/18
@Desc    :
'''

from network import Net
from zutil import *
import sys

from algo import Algo
from algoGreedy import AlgoGreedy
from algoBrute import AlgoBrute
from algoHeuristic import AlgoHeuristic
import pandas as pd

def run_algo(parser_algo):
    args, unk = parser_algo.parse_known_args()
    # logname = f"{args.did}_{args.method}_{args.obj}"
    # logname = f"{'+'.join(args.did_list)}_{'+'.join([str(int(x)) for x in args.lamb_list])}_{'+'.join(args.obj_list)}_{'+'.join(args.method_list)}"
    logname = f"{'+'.join(args.did_list)}"
    logger = get_log(logname)
    logger.info('python '+' '.join(sys.argv))

    for did in args.did_list:
        net = Net(logger, did, args.seed, args.portion )
        if 'brute' in args.method_list:
            algo = AlgoBrute(logger, net, args.quota_list)
            algo.run_dump()
        for method_g in [method for method in args.method_list if 'g' in method]:

            algo = AlgoGreedy(logger, net, args.quota_list, method_g, args.ssize_list, args.budget_list, args.a)
            if method_g == 'g0':
                algo.run_dump_g0()
            elif method_g == 'g1':
                algo.run_dump_g1()

        for method_h in [method for method in args.method_list if 'h' in method]:
            algo = AlgoHeuristic(logger, net, args.quota_list, method_h)  # , args.centrality_list
            algo.run_dump()






def add_args_general(subparser):
    subparser.add_argument('-s', "--seed", metavar='',
                           default='32', help="Seed for all random, usually fixed.")

    subparser.add_argument('-d', "--did", metavar='',
                           choices=['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'], help="Data to experiment.")
    subparser.add_argument('-dl', "--did_list", metavar='',
                           nargs='+', choices=['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'], help="Data list to experiment.")

    subparser.add_argument('-ml', "--method_list", metavar='',
                           nargs='+', choices=['brute', 'g0', 'g1', 'h0', 'h1', 'h2', 'h3'], help="Method list for subprob1.")

    subparser.add_argument('-ql', "--quota_list", metavar='',
                           nargs='+', type=int, help="list of m.")

    subparser.add_argument('-sl', "--ssize_list", metavar='',
                           nargs='+', type=int, help="List of sketch_size.")

    subparser.add_argument('-bl', "--budget_list", metavar='',
                           nargs='+', type=int, help="List of T.")

    subparser.add_argument('-p', "--portion", metavar='',
                           type=float, help="Portion of avialble.")
    subparser.add_argument('-pl', "--portion_list", metavar='',
                           nargs='+', type=float, help="List of portion of avialble.")

    subparser.add_argument('-a', "--a", metavar='',
                           type=float, help="parameter.")

def add_args_algo(subparser):
    add_args_general(subparser)

if __name__ == "__main__":
    logcmd()

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    subparsers = parser.add_subparsers(help='sub-commands', dest='cmd')
    parser_algo = subparsers.add_parser('algo', help='algo module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_plot = subparsers.add_parser('plot', help='plot module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args, unk = parser.parse_known_args()

    if args.cmd == "algo":
        add_args_algo(parser_algo)
        s = parser_algo.format_help().replace('\n\n', '\n')
        # print(f"{'*' * 50}\n{s}")
        run_algo(parser_algo)
    if args.cmd == "plot":
        pass



