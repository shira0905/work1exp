#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/13 15:10
@Desc    :   For results presentation: (1) format the experiment results, (2) plot as figures
'''

import numpy as np
import pandas as pd
# from trash.netoperatorREV import NetoperatorREV
import itertools
import math
import os
import pickle
from matplotlib import cm
import matplotlib.pyplot as plt


class Ploter:
    font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 20}
    font_legend = {'family': 'Times New Roman', 'weight': 'bold', 'size': 18}
    hatch_list = ['', "///", "\\\\\\", '---', '...', '*']

    def __init__(self ):
        # self.logger = logger
        self.PLT_DIR = "../eplots/plt"




    def plot_dsize2time(self):
        """ each epsilon plot one figure
        """
        xlabel = "dsize" # 应该就只能是这个了
        ylabel = "time"  # or "social welfare"

        D = {
            10000:1.333*234.37409300000002,
            37700:1.333*5566.048207000002,
            75888:1.333*15688.771837999995
        }
        plt.rc('font', **Ploter.font)
        plt.plot(D.keys(), D.values(), marker='o', lw=1.4,ms=7, color='black')
        # plt.legend()
        plt.xlabel("U", **Ploter.font)
        plt.ylabel("running time/s", **Ploter.font)
        plt.savefig(f"{self.PLT_DIR}/X{xlabel}_Y{ylabel}_k60_T4_m5.pdf", dpi=300, bbox_inches="tight", format='pdf')
        # plt.savefig(f"{self.PLT_DIR}/X{xlabel}_Y{ylabel}_k20_T3_m5.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()


    def plot_k2time(self):
        """ each epsilon plot one figure
        """
        xlabel = "k" # 应该就只能是这个了
        ylabel = "time"  # or "social welfare"

        D = {
            10:316,
            20:319.08413499999983, # 422
            30:323,
            40:332.6204839999996, # 417
            50:342,
            60:365.6145860000006, # 450
        }

        plt.rc('font', **Ploter.font)
        plt.plot(D.keys(), D.values(), marker='o', lw=1.4,ms=7, color='black')
        plt.ylim(ymin=0, ymax =max(D.values())*1.05 )
        # plt.legend()
        plt.xlabel(xlabel, **Ploter.font)
        plt.ylabel("running time/s", **Ploter.font)
        plt.savefig(f"{self.PLT_DIR}/X{xlabel}_Y{ylabel}_d3_T4_m5.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

    def plot_T2time(self):
        """ each epsilon plot one figure
        """
        xlabel = "T"  # 应该就只能是这个了
        ylabel = "time"  # or "social welfare"
        D = {
            10000: 76.36769099999992   , #420
            20000: 171.66498000000024  , #459
            30000: 269.45838300000014  , #459
            40000: 365.6145860000006    #450
        }

        plt.rc('font', **Ploter.font)
        plt.plot(D.keys(), D.values(), marker='o', lw=1.4,ms=7, color='black')
        plt.ylim(ymin=0, ymax =max(D.values())*1.05 )

        # plt.legend()
        plt.xlabel(xlabel, **Ploter.font)
        plt.ylabel("running time/s", **Ploter.font)
        # k60
        plt.savefig(f"../eplots/plt/X{xlabel}_Y{ylabel}_d3_k60_m5.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

    def plot_m2time(self):
        """ each epsilon plot one figure
        """
        xlabel = "m"  # 应该就只能是这个了
        ylabel = "time"  # or "social welfare"

        # D = {
        #     1: 63.078453999999965 ,  #232
        #     2: 129.1789450000001  , #302
        #     3: 202.5621700000006  , #368
        #     4: 281.6525760000004  , #415
        #     5: 365.6145860000006   #450
        # }
        D = {
        1: 59.497702 ,
        2: 123.51785100000001 ,
        3: 194.139408 ,
        4: 269.803177 ,
        5: 353.09481000000005 ,
        6: 436.6305960000001 ,
        7: 529.974904 ,
        8: 627.469403 ,
        9: 726.173029 ,
        10: 827.2389230000001 ,
        11: 930.274987 ,
        12: 1036.117833
        }

        plt.rc('font', **Ploter.font)
        plt.plot(D.keys(), D.values(), marker='o', lw=1.4,ms=7, color='black')
        plt.ylim(ymin=0, ymax =max(D.values())*1.05 )

        # plt.legend()
        plt.xlabel(xlabel, **Ploter.font)
        plt.ylabel("running time/s", **Ploter.font)
        plt.savefig(f"../eplots/plt/X{xlabel}_Y{ylabel}_d3_k60_T4.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()