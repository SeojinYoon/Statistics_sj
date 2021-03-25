
"""
목표: sequence만 부호화하는 것

제거해야 할 사항
숫자 하나만 입력하는 것 다 없애버려야함

수정해야 할 사항
- 시퀀스가 학습되었는지에 대한 보상 - 별로 표현(오른쪽 위)
- 버튼 입력 들어오면 포즈 같은거 해야함(누르고 있으면 계속 들어옴)
- 런 횟수 8개

수정 blue print
- 휴식 시간 20초
- 시퀀스 5초
- 1block - 시퀀스 48개(12분)

- block - 24개의 set 존재

set1: sequence 1 - sequence 2
set2: sequence 2 - sequence 1

"""


"""
Library Settings
"""

# source path 수정 필요
source_path = "/Users/yoonseojin/Statistics_sj/CLMN/Replay_Exp"

import os
os.chdir(source_path)

from Psychopy_Package.Psychopy_util import Sequence_st_text_unit, Sequence_st_bundle, St_Package, Experiment
from Preprocessing_Package.sj_util import get_random_sample_in_codes

"""
Data Setting
"""
# Making sequences
sequence1 = ["4", "1", "3", "2", "4"]
sequence2 = ["1", "4", "2", "3", "1"]
sequence_showing_time = 6

sequence1_color = [0,0,0]
sequence2_color = [1,1,1]

sequence_rest_time = 20

sequence_bundle_count_per_run = 12

seq_bundle1 = Sequence_st_bundle([
    Sequence_st_text_unit(sequence1, showing_time=sequence_showing_time, color=sequence1_color, text_height=0.1, is_count_correct=True),
    Sequence_st_text_unit(sequence2, showing_time=sequence_showing_time, color=sequence2_color, text_height=0.1, is_count_correct=True)
    ],
    ISI_interval= sequence_rest_time)

seq_bundle2 = Sequence_st_bundle([
    Sequence_st_text_unit(sequence2, showing_time=sequence_showing_time, color=sequence2_color, text_height=0.1, is_count_correct=True),
    Sequence_st_text_unit(sequence1, showing_time=sequence_showing_time, color=sequence1_color, text_height=0.1, is_count_correct=True)
    ],
    ISI_interval= sequence_rest_time)

# Make blocks
def make_blocks(seq_bundle1, seq_bundle2, run_count = 8):
    shuffles = []
    for i in range(0, run_count):
        samples_sets = get_random_sample_in_codes(sample_count=sequence_bundle_count_per_run,
                                                  codes=[1, 2],
                                                  ratio=[0.5, 0.5])
        seq_set_list = list(map(lambda x: seq_bundle1 if x == 1 else seq_bundle2, samples_sets))

        shuffles.append(seq_set_list)

    blocks = []
    for s in shuffles:
        blocks.append([St_Package(bundles=s, bundle_intervals=[0], interval_text="Empty")])
    return blocks

blocks = make_blocks(seq_bundle1, seq_bundle2, run_count=8)

# Experiments
data_dir_path = source_path
participant_name = "seojin"

exp = Experiment(monitor_size=[400,400],
                 is_full_screen = False,
                 data_dir_path = data_dir_path,
                 participant_name = participant_name,
                 ready_keys=["r"],
                 start_keys=["s"],
                 stop_keys=["p"],
                 valid_keys=["4", "3", "2", "1"],
                 input_device="keyboard")

exp.wait_blocks(blocks=blocks,
                iteration=0)
