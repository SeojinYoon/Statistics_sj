# Configuration(Need to setting)
project_home_path = "/Users/yoonseojin/Statistics_sj"
right_hand_data_dir_path = project_home_path + "/CLMN/Replay_Exp/experiment/20210403_blueprint_0324v2/right hand"
participant_name = "taehyun"

import os
os.chdir(project_home_path)

import pandas as pd

pd.set_option("display.width", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)

import numpy as np
import matplotlib.pyplot as plt

from CLMN.Replay_Exp.experiment.Replay_Experiment_Tool import mapping_data_current, single_response_only, \
    intertap_interval, plot_per_sequence, get_intertap_response, drawing_graph, draw_continuos_graph, draw_multi_graph, plot_learning, draw_avg_reaction
from File_Package.sj_file_system import CsvManager

seq1 = ["4", "1", "3", "2", "4"]
seq2 = ["1", "4", "2", "3", "1"]
seq1_name = "['4', '1', '3', '2', '4']"
seq2_name = "['1', '4', '2', '3', '1']"
seq1_color = "blue"
seq2_color = "red"

divided_count=4

"""
Load Data
"""
stimuluses = []
responses = []
for i in range(0, 4):
    stimulus_file_name = "stimulus_" + participant_name + "_" + str(i)
    response_file_name = "response_" + participant_name + "_" + str(i)
    stimuluses.append( CsvManager(dir_path=right_hand_data_dir_path, file_name=stimulus_file_name).read_csv_from_pandas()[2:-1] ) # remove not necessary data
    responses.append( CsvManager(dir_path=right_hand_data_dir_path, file_name=response_file_name).read_csv_from_pandas() )
stimuluses[-1] = stimuluses[-1][:-1] # remove not necessary data

mapped_d = mapping_data_current(stimuluses, responses)
mapped_d = single_response_only(mapped_d)
intertap_intervals = intertap_interval(mapped_datas=mapped_d,
                                       seq1=seq1,
                                       seq2=seq2,
                                       seq1_name=seq1_name,
                                       seq2_name=seq2_name)

"""
맞춘 시퀀스 드로잉
"""
run_index = 0
plot_per_sequence(run_index= run_index,
                  stimuluses=stimuluses,
                  intertap_intervals=intertap_intervals,
                  seq1_name=seq1_name,
                  seq2_name=seq2_name,
                  seq1_color=seq1_color,
                  seq2_color=seq2_color,
                  seq1=seq1,
                  seq2=seq2,
                  divided_count=divided_count)
plt.title("Taehyun, right, run " + str(run_index))

"""
맞춘 시퀀스 평균 드로잉
"""
run_index = 0
draw_avg_reaction(intertap_intervals,
                  divided_count=divided_count,
                  run_index=run_index,
                  stimuluses=stimuluses,
                  seq1_steps=list(stimuluses[run_index][stimuluses[run_index]["Stimulus"] == seq1_name]["Step"]),
                  seq1_name=seq1_name,
                  seq2_name=seq2_name,
                  seq1=seq1,
                  seq2=seq2,
                  seq1_color=seq1_color,
                  seq2_color=seq2_color)
plt.title("Taehyun, right, run " + str(run_index))


"""
Continuos average sequence

# 1
"""
from CLMN.Replay_Exp.experiment.Replay_Experiment_Tool import draw_continuos_mean_sequences
draw_continuos_mean_sequences(intertap_intervals= intertap_intervals,
                                divided_count= divided_count,
                                stimuluses= stimuluses,
                                seq1= seq1,
                                seq2= seq2,
                                seq1_name= seq1_name,
                                seq2_name= seq2_name,
                                seq1_color= seq1_color,
                                seq2_color= seq2_color)
plt.ylabel("avg intertap per sequence")
plt.xlabel("step number")
plt.title("Taehyun, right, run 0~3")

"""
스텝당 몇번 맞췄는지 표현

# 2
"""
divided_count = 4

run_indexes= []
steps = []
step_corrects = []
for run_index in range(0, len(stimuluses)):
    response_times = list(map(lambda x: list(map(lambda a: a[1], x["Response_times"])), intertap_intervals[run_index]))
    step_correct = list(map(lambda x: int(len(x) / divided_count), response_times))

    for i in range(0, len(step_correct)):
        run_indexes.append(run_index)
        steps.append(i*2)
        step_corrects.append(step_correct[i])

import pandas as pd
run_data = pd.Series(run_indexes)

data_ranges = []
for run_index in range(0, len(stimuluses)):
    start_index = run_data[run_data == run_index].index[0]
    end_index = run_data[run_data == run_index].index[-1]

    data_ranges.append([start_index, end_index])

colors=[]
for run_index in range(0, len(stimuluses)):
    t_steps = steps[data_ranges[run_index][0]: data_ranges[run_index][1]+1]
    heights = step_corrects[data_ranges[run_index][0]: data_ranges[run_index][1]+1]
    bar_width = 0.35

    color = ""
    if run_index == 0:
        color = "black"
    elif run_index == 1:
        color = "green"
    elif run_index == 2:
        color = "blue"
    elif run_index == 3:
        color = "purple"
    colors.append(color)

    plt.bar(x=np.array(t_steps) + bar_width*run_index, height=heights, width=bar_width, color=color)
plt.xticks(list(set(steps)), list(set(steps)))
import matplotlib.patches as mpatches
c1 = mpatches.Patch(color=colors[0], label="run 0")
c2 = mpatches.Patch(color=colors[1], label="run 1")
c3 = mpatches.Patch(color=colors[2], label="run 2")
c4 = mpatches.Patch(color=colors[3], label="run 3")
plt.legend(handles=[c1, c2, c3, c4])
plt.xlabel("Step number")
plt.ylabel("Correct count")
plt.title("Taehyun correct count run 0~3")

# Drawing
# Show raw data
tagett = "['4', '1', '3', '2', '4']"
run_index = 0
coords = get_intertap_response(run_index, intertap_intervals, divided_count=divided_count)
steps = np.array(list(map(lambda x: x["Step"], intertap_intervals[run_index])))
seq1_steps = np.array(list(stimuluses[run_index][stimuluses[run_index]["Stimulus"] == tagett]["Step"]))
drawing_graph(coords=coords,
              steps=steps,
              seq1_steps=seq1_steps,
              seq1_color=seq1_color,
              seq2_color=seq2_color,
              seq1=seq1,
              seq2=seq2)
plt.title("Taehyun right, run: 0")


"""
continuous graph
"""
draw_continuos_graph(stimuluses=stimuluses,
                     intertap_intervals=intertap_intervals,
                     seq1_name=seq1_name,
                     seq2_name=seq2_name,
                     divided_count=divided_count,
                     seq1_color=seq1_color,
                     seq2_color=seq2_color,
                     seq1=seq1,
                     seq2=seq2)
plt.title("Taehyun right, run 0~3")


"""
multi graph
"""
draw_multi_graph(stimuluses=stimuluses,
                 intertap_intervals=intertap_intervals,
                 run_indexes=[0,3],
                 seq1_name=seq1_name,
                 seq2_name=seq2_name,
                 divided_count=divided_count,
                 seq1=seq1,
                 seq2=seq2,
                 seq1_color=seq1_color,
                 seq2_color=seq2_color
                 )
plt.title("Taehyun right, run 0, 3")

"""
Total Learning
MOGs
MOnGs
"""
# + value는 learning이 개선된것
plot_learning(0, intertap_intervals, divided_count=divided_count)

"""
몇개 맞았는지 찍어보기

# 3
"""
from CLMN.Replay_Exp.experiment.Replay_Experiment_Tool import multi_response_only, time_difference
mapped_d = mapping_data_current(stimuluses, responses)
mapped_d = multi_response_only(mapped_d)
mapped_d = time_difference(mapped_d)

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
