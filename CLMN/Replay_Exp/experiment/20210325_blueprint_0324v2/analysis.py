

# Configuration(Need to setting)
project_home_path = "/Users/yoonseojin/Statistics_sj"
left_hand_data_dir_path = project_home_path + "/CLMN/Replay_Exp/experiment/20210325_blueprint_0324v2/left hand"  # Left Hand
participant_name = "jonghyuk"

import os
os.chdir(project_home_path)

import pandas as pd
pd.set_option("display.width", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)

import numpy as np
import matplotlib.pyplot as plt

from CLMN.Replay_Exp.experiment.Replay_Experiment_Tool import mapping_data_current, multi_response_only
from File_Package.sj_file_system import CsvManager

seq1_name = "['4', '1', '3', '2', '4']"
seq2_name = "['1', '4', '2', '3', '1']"
seq1_color = "blue"
seq2_color = "red"

"""
Load Data
"""
stimuluses = []
responses = []
for i in range(0, 4):
    stimulus_file_name = "stimulus_" + participant_name + "_" + str(i)
    response_file_name = "response_" + participant_name + "_" + str(i)
    stimuluses.append( CsvManager(dir_path=left_hand_data_dir_path, file_name=stimulus_file_name).read_csv_from_pandas()[2:-1] ) # remove not necessary data
    responses.append( CsvManager(dir_path=left_hand_data_dir_path, file_name=response_file_name).read_csv_from_pandas() )
stimuluses[-1] = stimuluses[-1][:-1] # remove not necessary data

def time_difference(mapped_datas):
    response_times_across_runs = []
    for run_index in range(0, len(mapped_datas)):
        response_times_per_run = []
        # groupby를 step으로 처리
        for name, group in mapped_datas[run_index].groupby("Step"):
            # Reaction time 정의
            # 한 스텝에서 처음 시퀀스가 완료된 경우: 현재 반응시간 - 자극 시간
            # 그 외의 경우: 현재 반응 시간 - 이전 반응시간
            for i in range(0, len(group)):
                if i == 0:
                    response_times_per_run.append(
                        group.iloc[0]["response_seconds"] - group.iloc[0]["stimulus_start_seconds"])
                else:
                    response_times_per_run.append(
                        group.iloc[i]["response_seconds"] - group.iloc[i - 1]["response_seconds"])
        response_times_across_runs.append(response_times_per_run)

    # 데이터에 삽입
    for run_index in range(0, len(mapped_datas)):
        mapped_datas[run_index]["Time Difference"] = response_times_across_runs[run_index]

    return mapped_datas

mapped_d = mapping_data_current(stimuluses, responses)
mapped_d = multi_response_only(mapped_d)
mapped_d = time_difference(mapped_d)

# 세션 마다 각 자극당 반응 시간을 찍어보기
# Stimulus를 그룹화하여 플롯팅
time_difference_per_run = []
run_index = 0
for run_index in range(0, len(stimuluses)):
    for name, group in mapped_d[run_index].groupby("Stimulus"):
        time_difference = group["Time Difference"]
        time_difference_per_run.append(list(map(lambda x: (run_index, name, x), time_difference)))

for i in range(0, len(time_difference_per_run)):
    data = time_difference_per_run[i]
    seq = time_difference_per_run[i][0][1]
    run_index = list(map(lambda x: x[0], data))
    response_data_group = list(map(lambda x: x[2], data))
    if seq == seq1_name:
        # 4-3-2-1-4
        plt.scatter(run_index, response_data_group, c=seq1_color, s=10)
    else:
        # 1-4-2-3-1
        plt.scatter(run_index, response_data_group, c=seq2_color, s=10)

plt.title(participant_name + "_replay_lefthand")
plt.xlabel("run index")
plt.ylabel("Reaction time")
plt.legend(["1-4-2-3-1", "4-3-2-1-4"])

# 세션마다 구간 별로 커팅
datas = []
for run_index in range(0, len(stimuluses)):
    datas.append(pd.value_counts(pd.cut(mapped_d[run_index]["Time Difference"], np.arange(0.5, 4, 0.2))).sort_index())

colors = plt.cm.jet(np.linspace(0,1,len(datas)))
for i in range(0, len(datas)):
    plt.plot(np.arange(0, len(datas[i])), datas[i], color=colors[i])
plt.legend(list(map(lambda x: "run " + str(x), range(0, len(datas)))))
plt.xticks(np.arange(len(datas[0].index)), datas[0].index, rotation='vertical')
plt.ylabel("count")
plt.title("jonghyuck count range of reaction time")
plt.xlabel("range of reaction time")

# 런 마다 자극 마다 구간별로 커팅
datas = []
for run_index in range(0, len(stimuluses)):
    for name, group in mapped_d[run_index].groupby("Stimulus"):
        datas.append([run_index, name, pd.value_counts(pd.cut(group["Time Difference"], np.arange(0.5,4,0.1))).sort_index()])

def plot_seq_difference(datas, run_index, seq1_special_color, seq2_special_color):
    target_datas = list(filter(lambda x: x[0] == run_index, datas))
    is_seq1_first = False
    i=0
    for data in target_datas:
        group_name = data[1]
        category_datas = data[2]
        if group_name == seq1_name:
            if is_seq1_first == False and i ==0:
                is_seq1_first = True
            plt.plot(np.arange(len(category_datas)), category_datas, color=seq1_special_color)
        else:
            plt.plot(np.arange(len(category_datas)), category_datas, color=seq2_special_color)
        i+=1
    plt.xticks(np.arange(len(category_datas)), category_datas.index, rotation='vertical')
    return is_seq1_first

colors = plt.cm.jet(np.linspace(0,1,len(datas)))
colors2 = plt.cm.jet(np.linspace(1,0,len(datas)))
is_seq1_firsts = []
for i in range(0, len(stimuluses)):
    is_seq1_firsts.append(plot_seq_difference(datas, i, seq1_special_color = colors[i], seq2_special_color = colors2[i]))
seq_labels = list(map(lambda x: [seq2_name, seq1_name] if x == "False" else [seq1_name, seq2_name], is_seq1_firsts))
import functools
import operator
seq_labels = functools.reduce(operator.iconcat, seq_labels, [])
seq_labels_last = []
for i in range(0, len(seq_labels)):
    session_i = str(int(i / 2))
    seq_labels_last.append(session_i + "_" + seq_labels[i])
plt.legend(seq_labels_last)
plt.ylabel("count of correct")

# Sequence 하나씩만 찍어보기
def plot_only_specific_seq(datas, run_index, special_color, is_only_seq1 = True):
    target_datas = list(filter(lambda x: x[0] == run_index, datas))

    for data in target_datas:
        group_name = data[1]
        category_datas = data[2]
        if group_name == seq1_name:
            if is_only_seq1:
                plt.plot(np.arange(len(category_datas)), category_datas, color=special_color)
        else:
            if is_only_seq1 == False:
                plt.plot(np.arange(len(category_datas)), category_datas, color=special_color)
    plt.xticks(np.arange(len(category_datas)), category_datas.index, rotation='vertical')
colors = plt.cm.jet(np.linspace(0,1,len(datas)))
for i in range(0, len(stimuluses)):
    plot_only_specific_seq(datas, i, special_color = colors[i], is_only_seq1=False)
plt.legend(list(map(lambda x: "session: "+ str(x), np.arange(len(stimuluses)))))
plt.title("jonghyuck seq2")

# 런 마다 각 자극당 몇번 반응하였는지 찍어보기
response_count = {}
run_index = 0
for run_index in range(0, len(stimuluses)):
    response_count[run_index] = pd.value_counts(mapped_d[run_index]["Stimulus"])

response_seq1s = []
response_seq2s = []
for run_index in range(0, len(stimuluses)):
    response_seq1s.append(response_count[run_index][seq1_name])
    response_seq2s.append(response_count[run_index][seq2_name])

run_indexes = np.arange(len(stimuluses))
bar_width = 0.35
plt.bar(x=run_indexes, height=response_seq1s, width=bar_width, color=seq1_color)
plt.bar(x=run_indexes + bar_width, height=response_seq2s, width=bar_width, color=seq2_color)
plt.xticks(run_indexes + bar_width/2, ('1', '2', '3', '4'))
plt.xlabel("run")
plt.ylabel("count of correct correct response")
plt.legend(["4-3-2-1-4", "1-4-2-3-1"], loc='upper left')
plt.title("jonghyuck, count correct response")






