
"""
Experiment Description

two-alternative forced-chocie frequency discrimination task

피험자는 진동자극의 빈도를 구별하였으며 왼쪽 집게 손가락에 순차적으로 자극이 가해짐
한번의 trial에서 2번의 순차적인 자극이 가해지며 그후 피험자는 결정을 내림

1개의 Block에 10번의 Trial 존재
ex)
Block1:
    trial 1: <----> f1(자극) <----> f2(자극) <---->
    trial 2: <----> f1(자극) <----> f2(자극) <---->
    ...
    trial 10: <----> f1(자극) <----> f2(자극) <---->
"""

"""
Meaning of Data

- Block
- Trial
- f_1(Hz): 두가지 선택안 중의 첫번째
- first ISI: 첫번째 자극간 간격
- f_2(Hz): 두가지 선택안 중의 두번째
- second ISI: 두번째 자극간 간격
- Subject's decision: 피험자의 결정(before: f_1(Hz) 선택, after: f_2(Hz) 선택, NaN: 결정을 내리지 못함)
- A time taken to make a decision: 결정에 걸리는 시간(sec)
- A third ISI time: 세번째 자극간 간격
"""

"""
Data Basic analysis (range, min, upper ...)

- Block의 범위는 1~10
- 각 피험자는 10번의 실험을 수행함
- 진동 자극의 범위는 10~20
- A time taken to make a decision: 
    최소: 0.005
    최대: 1.5
    표본평균: 0.5950
    표본분산: 0.0463
    
- 모든 row에 15hz의 진동수가 있다. (f_1, f_2를 불문하고), 즉 기준자극은 15Hz
- 기준 자극 15Hz를 제외하고, 각 진동수마다 비교자극 실험이 10번 시행됨       
- 아마 피험자는 더 진동수가 긴 자극을 판정하는 과제를 수행했던것 같다.
- 각 진동수마다 각 블록에 한번의 시도를 함
"""

"""
정신 능력 추정 함수

문제에서 주어진 정신 능력 추정 함수는 미분가능하다!
미분 가능하면? -> Neton Raphson method를 쓸수 있다.
    미분 가능한지 어떻게 알았는가?
    해당 함수가 연속인지 조사해보고, 좌미분계수와 우미분계수가 같은지 파악해 보았다.
    계산 결과 해당 함수는 연속이며, 미분가능하다. 
"""

import os
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
from Preprcoessing_Package import sj_preprocessing
from Preprcoessing_Package import sj_util
from Visualization_Package import F_Visualize
from Preprcoessing_Package import sj_dictionary
from Preprcoessing_Package import F_Algo
from Statistics_Package import stat_module
import seaborn as sns
from Higher_function import sj_higher_function
from PythonSequence import sj_sequence
import math

pd.set_option("display.width", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)

data_path = os.path.join(".", "CLMN_lab_test", "Data")
description_statistics_path = os.path.join(".", "CLMN_lab_test", "Discription_statistics")

def weibull_cdf(x, g, a, b):
    if x == 0:
        return g
    elif x < 0:
        return g * math.exp((-a)*pow(-x, b))
    else:
        return 1-(1-g)*math.exp((-a)*pow(x, b))

F_Visualize.draw_function(x=np.linspace(-100, 100, 1000), function= lambda x: weibull_cdf(x, 0.5, 3, 1))

"""
TML16에 대한 분석
"""

target_data_path = os.path.join(data_path, "TML16_Dis.txt")

data = pd.read_csv(target_data_path, sep="\t", header=None)
data.columns = ["Block", "Trial", "f_1(Hz)", "first ISI", "f_2(Hz)", "second ISI", "Subject's decision", "A time taken to make a decision", "A third ISI time"]

# Applied stimulus column 추가
data['Applied stimulus'] = sj_preprocessing.choice(data['f_1(Hz)'], data['f_2(Hz)'], data['f_1(Hz)'] != 15.0)

# Chocie Frequency 추가
TM16_choice_freq = sj_preprocessing.choice(data["f_1(Hz)"], data["f_2(Hz)"], data["Subject's decision"] == "before")
data["Choice Frequency"] = TM16_choice_freq

# TML16의 반응 시간을 구간으로 나눠 파악(10Hz)
ranges = sj_higher_function.recursive_map(sj_util.partition_d1(0, 1, 10), lambda x: round(x,1))
TML16_Hz10_decision_time = data[np.array(data['Applied stimulus']) == 10]['A time taken to make a decision']
counting = sj_preprocessing.counter(TML16_Hz10_decision_time, ranges, "None")
plt.bar(list(map(lambda x: str(x), counting.keys())),
        counting.values())
plt.xticks(fontsize=4, rotation=90)
plt.ylabel("count")
plt.xlabel("range of decision time")
plt.title("distribution about 10Hz of TML16")

# TML16의 A time taken to make a decision에 대한 평균
tml16_mean = data[["Applied stimulus", "A time taken to make a decision"]].groupby("Applied stimulus").aggregate(["mean"])
F_Visualize.draw_scatter_plot(tml16_mean.index,
                              tml16_mean[('A time taken to make a decision', 'mean')],
                              title = "TML16 mean of decision time", xlabel= "frequency", ylabel= "mean(s)")

# TML16의 A time taken to make a decision에 대한 box plot
sns.boxplot(x= "Applied stimulus", y= "A time taken to make a decision", data= data).set_title("Decision plot for TML16")

# 각 자극 수준에 대하여, 해당 자극이 선택된 개수를 count
dic_counter = sj_dictionary.init_dic(list(set(data["Applied stimulus"])), 0)
for key, partial_df in data.groupby("Applied stimulus"):
     dic_counter[key] = sum(partial_df["Choice Frequency"] == key)

proportion_higher_response = list(map(lambda x: x/10 , dic_counter.values()))
F_Visualize.draw_scatter_plot(dic_counter.keys(),
                              proportion_higher_response,
                              title = "TML16 proportion 'higer' response", xlabel= "Frequency(Hz)", ylabel= "proportion 'higher' response")
plt.grid()

"""
LSE에 대한 Contour plot 그리기

x # difference between two stimuli
x = f - 15
g = 0.5
a = 0~1
b = 0~8
"""

x = np.array(list(dic_counter.keys())) - 15
y = proportion_higher_response

length = 50
a = np.linspace(0, 1, length)
b = np.linspace(0, 8, length)
A, B = np.meshgrid(a,b)

result = np.array(np.repeat(0, length*length).reshape(length,length), dtype=np.float)
for i in range(0, len(a)):
    for j in range(0, len(b)):
        result[i][j] = np.log(stat_module.LSE(weibull_cdf, x, [0.5, A[i,j], B[i,j]], y))

plt.contour(B, A, result, 5, cmap='RdGy')
plt.colorbar()
plt.xlabel("β")
plt.ylabel("α")
plt.title("contour plot about χ^2 for TML16")

"""
LSE 3D plot 그리기
변수(a, b)
"""
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(B, A, result)

"""
find argument using gradient descent
"""
f = lambda a,b: np.log(stat_module.LSE(weibull_cdf, x, [0.5, a, b], y))

from ML_Package import sj_ml
a, b = sj_ml.gradient_descent(f, [1,1], 0.01, step_num=1000)

"""
draw fitted weibull_cdf
calculate JND
"""
def weibull_cdf2(x, g, a, b):
    # 그래프랑 맞추기 위해 사용
    x = x-15
    if x == 0:
        return g
    elif x < 0:
        return g * math.exp((-a)*pow(-x, b))
    else:
        return 1-(1-g)*math.exp((-a)*pow(x, b))

def JND(a, b):
    return ((1/a) * np.log(2)) ** (1/b)

F_Visualize.draw_function(x=np.linspace(10, 20, 1000), function= lambda x: weibull_cdf2(x, 0.5, a, b))
F_Visualize.draw_scatter_plot(dic_counter.keys(),
                              proportion_higher_response,
                              title = "TML16 proportion 'higer' response", xlabel= "Frequency(Hz)", ylabel= "proportion 'higher' response")
plt.scatter(15, 0.5)
plt.annotate("α= " + str(round(a,3)) + "\n"
             + "β= " + str(round(b,3)) + "\n"
             + "JND= " + str(round(JND(a,b),3)) + "Hz",
             xy=(0.1,0.8),
             xycoords='axes fraction',
             fontsize=14)
plt.grid()

"""
draw SSE using contour plot
"""
hz = list(dic_counter.values())

sse_result = np.array(np.repeat(0, length*length).reshape(length,length), dtype=np.float)
for i in range(0, len(A)):
    for j in range(0, len(B)):
        y_hat = [weibull_cdf2(hz, 0.5, A[i,j], B[i,j]) for hz in dic_counter]
        sse_result[i][j] = stat_module.SSE(np.array(hz), np.array(y_hat))

plt.contour(B, A, sse_result, 5, cmap='RdGy')
plt.colorbar()
plt.scatter(b,a)
plt.xlabel("β")
plt.ylabel("α")
plt.annotate("α= " + str(round(a,3)) + "\n"
             + "β= " + str(round(b,3)) + "\n"
             + "JND= " + str(round(JND(a,b),3)) + "Hz",
             xy=(0.1,0.8),
             xycoords='axes fraction',
             fontsize=14)
plt.title("contour plot about SSE for TML16")
