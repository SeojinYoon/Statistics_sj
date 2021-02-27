"""
Library Settings
"""

# source path 수정 필요
source_path = "/Users/yoonseojin/Statistics_sj/CLMN/Replay_Exp"

import os
os.chdir(source_path)

from Psychopy_Package.Psychopy_util import Text_st_bundle, Text_st_unit, \
    Sequence_st_text_unit, Sequence_st_bundle, St_Pakcage, Experiment
from Preprocessing_Package.sj_util import get_random_sample_in_codes
from Preprocessing_Package.sj_shuffle import shuffle_list
import itertools
from Higher_function.sj_higher_function import recursive_map

"""
Data Setting
"""
# making units

unit_data = ["1", "2", "3", "4"]
list_units = list(itertools.permutations(unit_data, 4))
shuffle_list(list_units)

units = recursive_map(list_units, lambda x: Text_st_unit(x, showing_time=0.5))


ISIs = []
ISI_file_path = os.path.join(source_path, "ISI.txt")
with open(ISI_file_path, "r") as f:
    ISIs = f.readlines()
    ISIs = list(map(lambda x: int(x), ISIs))

u_sets = []
for i in range(0, len(units)):
    j = i * 3

    u_s = units[i]
    u_sets.append(Text_st_bundle(units=u_s,
                                 ISI_times=[ISIs[j], ISIs[j+1], ISIs[j+2]]))

# Making sequences
seq1 = Sequence_st_bundle([Sequence_st_text_unit(["4", "3", "2", "1", "4"], showing_time=15, color=[0,0,0], text_height=0.1)],
                          ISI_interval= 21)
seq2 = Sequence_st_bundle([Sequence_st_text_unit(["1", "4", "2", "3", "1"], showing_time=15, color=[1,1,1], text_height=0.1)],
                          ISI_interval= 21)

samples = get_random_sample_in_codes(6, [1,2], [0.5,0.5])
seq_set_list = list(map(lambda x: [seq2, seq1] if x == 1 else [seq1, seq2], samples))

shuffle_list(seq_set_list)

# combine unit and sequence
def make_blocks(u_sets, seq_set_list):
    combination_units = []

    seq_list = []
    for seq_set in seq_set_list:
        seq_list.append(seq_set[0])
        seq_list.append(seq_set[1])

    sequence_length = len(seq_list)
    unit_set_length = len(u_sets)

    time_interval_between_bundles = [10, 0]

    blocks = []
    if unit_set_length > sequence_length and (unit_set_length % sequence_length) == 0:
        for i in range(0, sequence_length):
            combination_unit = (u_sets[i], seq_list[i])
            combination_units.append(combination_unit)
        blocks.append(list(map(lambda x: St_Pakcage(bundles=[x[0], x[1]],
                                                    bundle_intervals=time_interval_between_bundles,
                                                    interval_text="..."), combination_units)))

        # Sequence is mached all, so they need to be shuffled
        shuffle_list(seq_list)

        combination_units = []
        for i in range(0, len(seq_list)):
            combination_unit = (u_sets[i+sequence_length], seq_list[i])
            combination_units.append(combination_unit)
        blocks.append(list(map(lambda x: St_Pakcage(bundles=[x[0], x[1]],
                                                     bundle_intervals=time_interval_between_bundles,
                                                     interval_text="..."), combination_units)))

        # u_sets and sequence are mached all, so they need to be shuffled
        shuffle_list(u_sets)
        shuffle_list(seq_list)
    return blocks

blocks = []
for t in range(0,4):
    blocks += make_blocks(u_sets, seq_set_list)

# 나중에 사용할때 이것만 고쳐주면 됨

data_dir_path = source_path
participant_name = "seojin"

exp = Experiment(monitor_size=[400,400],
                 is_full_screen = False,
                 data_dir_path = data_dir_path,
                 participant_name = participant_name,
                 ready_keys=["r"],
                 start_keys=["s"],
                 stop_keys=["q"],
                 input_device="keyboard")

exp.wait_blocks(blocks=list(map(lambda x: [x[0]], blocks))[0:3],
                iteration=0,
                end_message="End")

"""
block_index = 6
exp.wait_pkg(pkgs=blocks[block_index],
             end_message="End")
"""
