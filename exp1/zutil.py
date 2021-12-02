#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:38
@Desc    :
'''
import argparse
import datetime
import logging
import subprocess
import sys
import matplotlib.pyplot as plt
import os
import re
import pickle
import pandas as pd

import json
PKLDIR = '../eplots/pkl'
CSVDIR = '../eplots/csv'

def mymain():
    pass

def visualize_pkl(pklsrc):
    dictionary = {}
    if pklsrc != None:
        dictionary = pickle.load(open(pklsrc, 'rb'))
    json_object = json.dumps(dictionary, indent=4)
    print(json_object)

def tocsv_optSolution(headrow, didrid_list, method_list):
    # quota_list 不用这个参数是因为不同的did 和 method, quota集合不一致
    fullrow_list = [headrow]
    for didrid in didrid_list:
        for method in method_list:
            pklsrc = get_latest_path(f"{PKLDIR}/", f'{didrid}_{method}', 'pkl')
            result = {}
            print(pklsrc)
            if pklsrc != None:
                result = pickle.load(open(pklsrc, 'rb'))

            if  method!='g0':
                for quota, optsolution in result.items():
                    print(optsolution)
                    t_proc = None if len(optsolution) ==2 else optsolution[2]
                    fullrow_list.append([didrid, method, None, None, quota, optsolution[0], optsolution[1], t_proc, None])
            else:
                print(result)
                for ssize, budgets2quotas2optsolution in result.items():
                    print(budgets2quotas2optsolution)
                    for budget, quotas2optsolution in budgets2quotas2optsolution.items():
                        t_accum = 0
                        for quota, optsolution in quotas2optsolution.items():
                            t_accum += optsolution[2]
                            fullrow_list.append([didrid, method, ssize, budget, quota, optsolution[0], optsolution[1], optsolution[2], t_accum])

    data = pd.DataFrame(fullrow_list)
    csvsrc = f"{PKLDIR}/temp.csv"
    data.to_csv(csvsrc, index=False, header=False, sep='\t')

def tocsv_rawBrute(headrow, did_list, quota_list):
    fullrow_list = [headrow]
    for did in did_list:
        for quota in quota_list:
            pklsrc = get_latest_path(f"{PKLDIR}/detail_brute", f'{did}_{quota}', 'pkl')
            setMs2obj = {}
            if pklsrc != None:
                setMs2obj = pickle.load(open(pklsrc, 'rb'))
            for setM, obj in setMs2obj.items():
                fullrow_list.append([did, quota, setM, obj])
    data = pd.DataFrame(fullrow_list)
    csvsrc = f"{PKLDIR}/detail_brute/temp.csv"
    data.to_csv(csvsrc, index=False, header=False, sep='\t')

def logcmd():
    nowTime = datetime.datetime.now().strftime("%m%d-%H%M%S")
    cmd = f"\n\n{nowTime}\npython {' '.join(sys.argv)}"
    with open("RESULT.log", "a") as myfile:
        myfile.write(cmd)


def get_latest_path(dir, prefix, suffix):
    result_filename_list = []
    for filename in os.listdir(dir):
        if prefix in filename and suffix in filename:
            result_filename_list.append(filename)
    result_filename_list.sort()
    # print(result_filename_list)
    if len(result_filename_list) > 0:
        return f"{dir}/{result_filename_list[-1]}"
    return None



def clean_old_pkl(did_list, method_list):
    for did in did_list:
        for method in method_list:
            prefix = f"{did}_{method}"
            pklsrc = get_latest_path(PKLDIR, prefix, 'pkl')
            for filename in os.listdir(PKLDIR):
                if prefix in filename and filename not in pklsrc:
                    os.remove(f"{PKLDIR}/{filename}")

def cmd(logger, command, simulation=0):
    """wrap subprocess
    """
    if logger:
        logger.info('Subprocess: \"' + command + '\"')
    else:
        print('Subprocess: \"' + command + '\"')
    if simulation == 0:
        subprocess.run(command, shell=True)

def get_log(logname):
    """Custom a logger,  return the name of the log file
    """
    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    logger = logging.getLogger(logname)  # 设定logger的名字
    logger.setLevel(logging.INFO)  # 设定logger得等级
    ch = logging.StreamHandler()  # 输出流的hander，用与设定logger的各种信息
    ch.setLevel(logging.INFO)  # 设定输出hander的level
    logname = f"../elogs/{nowTime}_{logname}.log"
    fh = logging.FileHandler(logname, mode='a')  # 文件流的hander，输出得文件名称，以及mode设置为覆盖模式
    fh.setLevel(logging.INFO)  # 设定文件hander得lever
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)  # 两个hander设置个是，输出得信息包括，时间，信息得等级，以及message
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 将两个hander添加到我们声明的logger中去
    logger.addHandler(ch)
    var = logger.name
    print(logname)
    return logger

def detectHeadLines(filename):
    # remove the existing span tags
    f = open(filename, 'r', encoding='utf-8')
    text = ''
    clean = re.compile('<.*?>')
    for line in f.readlines():
        if '#head' not in line:
            if 'span' in line:
                line = re.sub(clean, '', line)
            text += line
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

    # add new tag
    f = open(filename, 'r', encoding='utf-8')
    headline_dic = {'#': 0, '##': 1, '###': 2, '####': 3, '#####': 4, '######': 5}
    suojin = {0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1}

    f.seek(0)

    insert_str = ""
    org_str = ""

    last_status = -1
    c_status = -1

    headline_counter = 0
    iscode = False
    for line in f.readlines():
        if (line[:3] == '```'):
            iscode = not iscode

        # fix code indent bug and fix other indentation bug. 2020/7/3
        if not iscode:
            temp_line = line.strip(' ')
        ls = temp_line.split(' ')
        if len(ls) > 1 and ls[0] in headline_dic.keys() and not iscode:
            headline_counter += 1
            c_status = headline_dic[ls[0]]
            # find first rank headline
            if last_status == -1 or c_status == 0 or suojin[c_status] == 0:
                # init suojin
                for key in suojin.keys():
                    suojin[key] = -1
                suojin[c_status] = 0
            elif c_status > last_status:
                suojin[c_status] = suojin[last_status] + 1

            # update headline text
            headtext = ' '.join(ls[1:-1])
            if ls[-1][-1] == '\n':
                headtext += (' ' + ls[-1][:-1])
            else:
                headtext += (' ' + ls[-1])
            headid = '{}{}'.format('head', headline_counter)
            headline = ls[0] + ' <span id=\"{}\"'.format(headid) + '>' + headtext + '</span>' + '\n'
            org_str += headline

            jump_str = '- [{}](#{}{})'.format(headtext, 'head', headline_counter)
            insert_str += ('\t' * suojin[c_status] + jump_str + '\n')

            last_status = c_status
        else:
            org_str += line

    insert_str = insert_str + org_str
    f.close()

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(insert_str)


def parse_args_all(parser):
    knownargs, unk = parser.parse_known_args()
    para_name_list = [x  for x in unk if '-' in x ]

    name2value = {}
    para_name = None
    para_value_list = []
    for elem in unk:
        if elem in para_name_list:
            # 先把上一个参数倒空, 如果没有上一个的话跳过, 那意味着最后一个没有被轮到
            if para_name:
                name2value[para_name] = para_value_list[0] if len(para_value_list)==1 else para_value_list
            para_name = elem
            para_value_list.clear()
        if elem not in para_name_list:
            para_value_list.append(elem)
    name2value[para_name] = para_value_list[0] if len(para_value_list)==1 else para_value_list
    # print(name2value)
    return knownargs, name2value

if __name__ == '__main__':
    mymain()



