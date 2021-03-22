
"""
목표: sequence만 부호화하는 것

제거해야 할 사항
숫자 하나만 입력하는 것 다 없애버려야함

수정해야 할 사항
- 시퀀스가 학습되었는지에 대한 보상 - 별로 표현(오른쪽 위)
- 맞으면 시퀀스가 변경되어 *로 표시됨
- 버튼 입력 들어오면 포즈 같은거 해야함(누르고 있으면 계속 들어옴)
- 런 횟수 8개

수정 blue print

"""


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
# Making sequences
seq1 = Sequence_st_bundle([Sequence_st_text_unit(["4", "3", "2", "1", "4"], showing_time=15, color=[0,0,0], text_height=0.1)],
                          ISI_interval= 21)
seq2 = Sequence_st_bundle([Sequence_st_text_unit(["1", "4", "2", "3", "1"], showing_time=15, color=[1,1,1], text_height=0.1)],
                          ISI_interval= 21)

samples = get_random_sample_in_codes(6, [1,2], [0.5,0.5])
seq_set_list = list(map(lambda x: [seq2, seq1] if x == 1 else [seq1, seq2], samples))

shuffle_list(seq_set_list)


# 나중에 사용할때 이것만 고쳐주면 됨

data_dir_path = source_path
participant_name = "eunha"

exp = Experiment(monitor_size=[1000,1000],
                 is_full_screen = True,
                 data_dir_path = data_dir_path,
                 participant_name = participant_name,
                 ready_keys=["r"],
                 start_keys=["s"],
                 stop_keys=["p"],
                 valid_keys=["4", "3", "2", "1"],
                 input_device="keyboard")

exp.wait_blocks(blocks=blocks,
                iteration=0)

"""
block_index = 6
exp.wait_pkg(pkgs=blocks[block_index], iteration = block_index)
"""