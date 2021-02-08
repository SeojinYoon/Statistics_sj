
"""
- category
: type
*! Thinking
*: Description
*@ Making code right now
*# Class

"""

"""
First check for computational problem

Library check
    - Psychopy
        - Input certification
            *@ Input test
            *@ Input must be robust about time(So, need to check input is doing well when the time is delayed)

        - Window
            *@ checking window is opened stably
            *@ checking window can be deleted

    - Making CSV file
        *@ I need to check the file writed by input

"""

"""
Consideration for Maintenance

- Experiment Design can be changed always
    - Especially, A time interval can be changed often 
        *! So, every experiment unit need to be changed easily
    - Experiment Unit can be changed often
        *! requirement for Design Pattern(Make base unit after then every unit need to be inherited the base unit
    
- Interface can be changed
    - if so, I need to construct the code independently about interface
        *! requirement for Design Pattern
"""

"""
Data construction
*: The data is inserted on same file about both One input and Sequence but the file need to header To discriminate them whose name is exp_type
The first data is T0 recorded when the experiment is started
The csv file's name is varied by participant_num  
    - exp_type
        - One input
        - Sequence
    - block_count
        *: max 8
    - stimulus: string
    - set_count
        *: max 6
    - step
        *: stimulus step(unit step)
    - seconds
        *: time.time() - start
"""

"""
Class Design
    *# St_Unit(St means stimulus)
        *: It is base unit of stimulus
        Every unit is showing something and they have some delay time
        so, the Base unit has some method
            - property
                - delay_time
            
            - Method
                - stimulus()
                    - Stimulus can be designed by image or text, so the return value can be image or text 
                - delay_time()
    
            - Child Class
                *# Image_st_unit
                    It denotes stimulus showing image
                        - stimulus()
                            return image_path
                            
                *# Text_st_unit
                    It denotes stimulus showing text
                        - Property
                            - text_color
                            
                        - Method
                            - stimulus()
                                *: return text
              
                *# Sequence_st_text_unit
                        - stimulus()
                            *: return list of text
                        - text_color()
                        
    *# Psy_display_manager
        *: It is interface of both st_unit and psychopy
            - Method
                - show_stimulus(st_unit)
                    *: if the st_unit's class should be Image_st_unit, psychopy will show image
                    if the st_unit's class should be Text_st_unit, psychopy will show text
                    and finally apply delay time to psychopy
                
     *# Input_interface_manager
        *: It is the class managing input interface
            - Property
                - stop_keys: list(string)
                - device: string
                    *: if the device is keyboard, psychopy is inputted by computer keyboard
                
            - Method
                - set_device(name)
                    *: It denotes that psychopy is reacted by what device is inputted
                - monitoring()
                    *: It is operating to listen any inputs until stop key is occured
                    It logs what is the input 
    
    *# Event_manager
        - Property
            - is_activate
            - is_activate_one_input
            - is_activate_multiple_input
            
        - Method
            - listen_input(input)
                *: It is called after a input is occured
            
            - listen_one_input(input)
                *: It is called after one input is occured
            
            - listen_multiple_input(inputs)
                *: It is called after many inputs are occured
            
            - set_is_activate_one_input()
                *: It denotes that listen_one_input can be activated
                
            - set_is_activate_multiple_input()
                *: It denotes that listen_multiple_input can be activated
                
    *# Csv_manager
        - Property
            - path
            
        - Method
            - set_csv_path()
            - write_header()
            - write_row()
"""

from Psychopy_Package.Psychopy_util import Event_manager, Input_interface_manager, \
    Psy_display_manager, Text_st_bundle, Text_st_unit, \
    Sequence_st_text_unit, Sequence_st_bundle, St_Pakcage, Experiment
from Preprcoessing_Package.sj_util import get_random_sample_in_codes
from Preprcoessing_Package.sj_shuffle import shuffle_list

# make block
def make_blocks(u_sets, seq_set_list):
    from Preprcoessing_Package.sj_shuffle import shuffle_list

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
                                                    bundle_intervals=time_interval_between_bundles), combination_units)))

        # Sequence is mached all, so they need to be shuffled
        shuffle_list(seq_list)

        combination_units = []
        for i in range(0, len(seq_list)):
            combination_unit = (u_sets[i+sequence_length], seq_list[i])
            combination_units.append(combination_unit)
        blocks.append([list(map(lambda x: St_Pakcage(bundles=[x[0], x[1]],
                                                     bundle_intervals=time_interval_between_bundles), combination_units))])

        # u_sets and sequence are mached all, so they need to be shuffled
        shuffle_list(u_sets)
        shuffle_list(seq_list)
    return blocks

# Data Setting

"""
Units
"""
import itertools
unit_data = ["1", "2", "3", "4"]
list_units = list(itertools.permutations(unit_data, 4))
shuffle_list(list_units)

# 유닛 만들기
# 유닛 만들고, 4개씩 묶어서 unit 단위 만들기(각 유닛 뒤에 delay time 주기)
from Higher_function.sj_higher_function import recursive_map
units = recursive_map(list_units, lambda x: Text_st_unit(x, showing_time=0.5))

u_sets = []
for u_s in units:
    u_sets.append(Text_st_bundle(units=u_s,
                                 rumination_avg_time=3,
                                 minimum_rumination_time=0.5,
                                 maximum_rumination_time=2))

"""
Sequences
"""
seq1 = Sequence_st_bundle([Sequence_st_text_unit(["4", "3", "2", "1", "4"], showing_time=15, color=[0,0,0])],
                          rumination_interval= 21)
seq2 = Sequence_st_bundle([Sequence_st_text_unit(["1", "4", "2", "3", "1"], showing_time=15, color=[1,1,1])],
                          rumination_interval= 21)

samples = get_random_sample_in_codes(6, [1,2], [0.5,0.5])
seq_set_list = list(map(lambda x: [seq2, seq1] if x == 1 else [seq1, seq2], samples))

shuffle_list(seq_set_list)

"""
unit set과 sequence 통합
"""
blocks = []
for t in range(0,4):
    blocks += (make_blocks(u_sets, seq_set_list))

block_index = 0 # 나중에 사용할때 이것만 고쳐주면 됨

"""
event_manager = Event_manager()
interface = Input_interface_manager(start_keys=["s"], stop_keys=["q"], event_manager=event_manager, device_name="keyboard")

p = Psy_display_manager(interface, event_manager)
p.open_window([200, 200], [-1,-1,-1])

p.wait_start(iteration=str(block_index+1))

p.show_stimuluses([Text_st_unit("1", showing_time=2), Text_st_unit("2", showing_time=3)])
p.show_packages(blocks[block_index])

interface.monitoring()

p.close_window()
"""
exp = Experiment([100,100], ["s"], ["q"])
"""
exp.wait_pkg(iteration="1",
             pkgs=blocks[block_index],
             end_message="End")
"""
exp.wait_stimuluses(iteration=str(block_index+1),
                    stimuluses=[Text_st_unit("1", showing_time=3)],
                    end_message="iteration" + str(block_index+1) + " End")
# single input event 정의(doSomething)
# multiple input event 정의(doSomething)
# CSV manager 작성
# Set1과 Set2의 색상 설정

