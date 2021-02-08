# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:12:48 2019

@author: STU24
"""

# Visualize 관련

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def draw_bar_plot(x_list, y_list, title = "Title", xlabel = "xlabel", ylabel = "ylabel"):
    plt.bar(x_list, y_list)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def draw_scatter_plot(x_list, y_list, title = "Title", xlabel = "xlabel", ylabel = "ylabel"):
    plt.scatter(x_list, y_list)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

# 선그래프를 그린다. 이때 주어지는 각 data_sets의 요소로 하나의 선이 구성된다.
# data_sets은 리스트로 주되 Series 형식이어야함 
def draw_line_graph(data_sets, 
                    x_marks = None, 
                    title = None,
                    ylim = None, 
                    xlabel = None, 
                    ylabel = None,
                    legend = None):
    for ds in data_sets:
        ds.index = list(range(0, len(ds)))
        
    # 각 데이터 셋을 하나의 DataFrame으로 만들어서 선그래프를 그리자
    df = pd.concat(data_sets, axis= 1)
    
    fig, ax = plt.subplots(1,1)
    ax.plot(df)
    
    # x축을 조정하고
    if x_marks is not None:
        plt.xticks(df.index, x_marks)
    
    # y축을 조정한다
    if ylim is not None:
        ax.set_ylim(ylim)
    
    if title is not None:
        plt.title(title)
    
    # 축 이름 설정
    if xlabel is not None:
        plt.xlabel(xlabel)
        
    if ylabel is not None:
        plt.ylabel(ylabel)
    
    if legend is not None:
        plt.legend(legend)
        
    return ax

# stack graph를 그림
# data_sets: data_set을 요소로 갖는 리스트, 
# legends: 범례로 들어갈 리스트
# x_marks: x축 눈금에 들어갈 이름
# x_label: x축 이름
# y_label: y축 이름
def draw_stack_graph(data_sets, 
                     legends = None,
                     title = None,
                     x_marks = None,
                     x_rotation = None,
                     x_label = None,
                     y_label = None):
    longest_set_length = 0
    for data_set in data_sets:
        data_length = len(data_set)
        if longest_set_length < data_length:
            longest_set_length = data_length
    
    indexes = range(0, longest_set_length)
    
    width = 0.35
    
    import matplotlib.pyplot as plt
    
    plts = []
    for i, data_set in enumerate(data_sets):
        if i == 0:
            c_plt = plt.bar(indexes, data_set, width)
        else:
            c_plt = plt.bar(indexes, data_set, width, bottom = data_sets[i-1])
        plts.append(c_plt)
    
    ps = [plt[0] for plt in plts]
    
    if legends is not None:
        plt.legend(tuple(ps), tuple(legends))
    
    if title is not None:
        plt.title(title)
    
    if x_rotation is not None and x_marks is not None:
        plt.xticks(indexes, x_marks, rotation = x_rotation)
    else:
        if x_marks is not None:
            plt.xticks(indexes, x_marks)
    
    if x_label is not None:
        plt.xlabel(x_label)
        
    if y_label is not None:
        plt.ylabel(y_label)
    
    return plt

def draw_function(x, function):
    """
    Drawing graph of function

    :param x: numpy array ex) np.linespace(-100, 100, 1000)
    :param function: function ex) lambda x: x+1
    """
    plt.plot(x, list(map(lambda element: function(element), x)))

if __name__=="__main__":
    import F_Visualize
    test = pd.DataFrame([
        [100, 200, 150],
        [123, 180, 159],
        [130, 190, 182],
        [134, 210, 167],
        [159, 230, 171],
        [160, 235, 180],
        [169, 237, 188]
                ])

    a = F_Visualize.draw_line_graph([test[0], test[1], test[2]], x_marks = ['아', '야', '어', '여', '오', '요'],
                        ylim = [0, 300],
                        xlabel = 'x축',
                        ylabel = 'y축',
                        title = 'abc')
    
    F_Visualize.draw_stack_graph([[1,2,3,4], [5,6,7,8]], 
                 legends = ['1234','456'], 
                 title = '1234', 
                 x_marks = ['가','나','다','라'], 
                 x_label = 'Y축!~', 
                 y_label = 'X축!~')

    F_Visualize.draw_function(np.linspace(0, 100, 100), lambda x: x + 1)


