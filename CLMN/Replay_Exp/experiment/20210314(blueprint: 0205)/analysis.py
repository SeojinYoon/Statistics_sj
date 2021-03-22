
# Configuration(Need to setting)
project_home_path = "/Users/yoonseojin/Statistics_sj"
left_hand_data_dir_path = "/CLMN/Replay_Exp/experiment/20210314(blueprint: 0205)/left hand"  # Left Hand
participant_name = "eunha"

import os
os.chdir(project_home_path)

import pandas as pd
pd.set_option("display.width", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)

from Visualization_Package import F_Visualize
from CLMN.Replay_Exp.experiment.Replay_Experiment_Tool import mapping_data, multi_response_only, time_difference, avg_time_difference_per_sessions, accuracy
from File_Package.sj_file_system import CsvManager

stimuluses = []
responses = []
for i in range(0, 8):
    stimulus_file_name = "stimulus_" + participant_name + "_" + str(i)
    response_file_name = "response_" + participant_name + "_" + str(i)
    stimuluses.append( CsvManager(dir_path=left_hand_data_dir_path, file_name=stimulus_file_name).read_csv_from_pandas()[2:-1] ) # remove not necessary data
    responses.append( CsvManager(dir_path=left_hand_data_dir_path, file_name=response_file_name).read_csv_from_pandas() )
stimuluses[-1] = stimuluses[-1][:-1] # remove not necessary data

mapped_d = mapping_data(stimuluses, responses)
mapped_d = multi_response_only(mapped_d)
mapped_d = time_difference(mapped_d)
avg_time_difference_per_sess = avg_time_difference_per_sessions(mapped_d)

# Avg Time difference
F_Visualize.draw_line_graph(
    data_sets = [pd.Series(avg_time_difference_per_sess)],
    xlabel = "Session_index",
    ylabel= "Average Difference(R_t - S_t)",
    title = participant_name + "_sequence_left_replay"
)

# Stimulus를 그룹화하여 플롯팅
time_difference_per_session = []
session_index = 0
for session_index in range(0, len(stimuluses)):
    for name, group in mapped_d[session_index].groupby("Stimulus"):
        time_difference = group["Time Difference"]
        time_difference_per_session.append(list(map(lambda x: (session_index, name, x), time_difference)))

import matplotlib.pyplot as plt
for i in range(0, len(time_difference_per_session)):
    data = time_difference_per_session[i]
    session_index = list(map(lambda x: x[0], data))
    response_data_group = list(map(lambda x: x[2], data))
    if i % 2 == 0: # 시퀀스 구분
        # 1-4-2-3-1
        plt.scatter(session_index, response_data_group, c="red", s = 10)
    else:
        # 4-3-2-1-4
        plt.scatter(session_index, response_data_group, c="blue", s= 10)
plt.title(participant_name + "_replay_lefthand")
plt.xlabel("Session index")
plt.ylabel("Reaction time")
plt.plot(list(range(0, len(mapped_d))), avg_time_difference_per_sess)
plt.legend(["average", "1-4-2-3-1", "4-3-2-1-4"])

# Accuracy
sessions_indexes = list(range(0, len(mapped_d)))
F_Visualize.draw_bar_plot(
    x_list = sessions_indexes,
    y_list= pd.Series(accuracy(mapped_d)),
    xlabel = "Session_index",
    ylabel= "accuracy ratio",
    title = participant_name + "_sequence_replay_lefthand"
)
