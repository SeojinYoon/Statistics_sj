
"""
s = Image_st_unit("1234")
isinstance(s, Image_st_unit)
"""

import psychopy
from Preprcoessing_Package.sj_util import split_value
from threading import Timer
import queue

class St_Unit:
    def __init__(self, showing_time):
        self.showing_time = showing_time

class Image_st_unit(St_Unit):
    def __init__(self, image_path, showing_time = 0.0):
        self.image_path = image_path
        self.showing_time = showing_time

class Text_st_unit(St_Unit):
    def __init__(self, text, color=[1,1,1], showing_time = 0.0):
        self.text = text
        self.color = color
        self.showing_time = showing_time

class St_bundle:
    def __init__(self, units):
        self.units = units
        self.rumination_units = []

class Text_st_bundle(St_bundle):
    def __init__(self, units, rumination_avg_time, minimum_rumination_time, maximum_rumination_time, minimum_increase=0.1):
        """
        :param units: list of Text_st_unit
        :param rumination_avg_time: average time(Secs) for rumination. if this value is 3 the rumination average time is 3sec per bundle
        """
        # units: list of Text_st_unit
        self.units = units
        self.rumination_avg_time = rumination_avg_time
        self.rumination_times = split_value(split_value=rumination_avg_time,
                                            split_count=len(units),
                                            minimum_value=minimum_rumination_time,
                                            maximum_value=maximum_rumination_time,
                                            minimum_increase=minimum_increase)
        ruminations_stimulus = []
        for i in range(0, len(units)):
            ruminations_stimulus.append(Text_st_unit("+", showing_time=self.rumination_times[i]))
        self.rumination_units = ruminations_stimulus

class Sequence_st_text_unit(St_Unit):
    #: ex) 3-2-1-4-3
    def __init__(self, text_units, showing_time = 0.0, color = [1,1,1]):
        self.showing_time = showing_time
        self.color = color

        type_check = [isinstance(t_u, Text_st_unit) for t_u in text_units]
        if sum(type_check) == len(text_units):
            result = []
            for unit in text_units:
                result += unit.text
            self.texts = result
        else:
            type_check = [isinstance(t, str) for t in text_units]
            if sum(type_check) == len(text_units):
                self.texts = text_units
            else:
                raise Exception("Type Error!")

class Sequence_st_bundle(St_bundle):
    def __init__(self, sequences, rumination_interval):
        super().__init__(sequences)
        for i in range(0, len(sequences)):
            self.rumination_units.append(Text_st_unit(text="+", showing_time=rumination_interval))

class St_Pakcage:
    def __init__(self, bundles, bundle_intervals):
        self.bundles = bundles
        self.bundle_intervals = bundle_intervals

        interval_units = []
        for i in range(0, len(bundles)):
            remain = i % len(bundle_intervals)

            interval_units.append(Text_st_unit(text="+", showing_time=bundle_intervals[remain]))
        self.interval_units = interval_units

class Psy_display_manager:
    def __init__(self, input_interface_manager, event_manager):
        self.input_interface_manager = input_interface_manager
        self.event_manager = event_manager

    def open_window(self, size, color = [-1,-1,-1] ):
        print("open window")
        from psychopy import visual

        self.visual = visual
        self.win = self.visual.Window(size=size,
                                      color=color,
                                      colorSpace='rgb')

    def wait_start(self, iteration):
        self.show_stimulus(Text_st_unit(str(iteration) + " trial" + " Ready" ))
        self.input_interface_manager.wait_start()

    def show_stimulus(self, stimulus, text_height=0.3, bold=True):
        if isinstance(stimulus, Image_st_unit):
            self.event_manager.set_is_activate_one_input(True)
            self.event_manager.set_is_activate_multiple_input(False, 0)
            print(str.format("showed: {0}, showing time: {1}", stimulus.image_path, stimulus.showing_time))
        elif isinstance(stimulus, Text_st_unit):
            self.event_manager.set_is_activate_one_input(True)
            self.event_manager.set_is_activate_multiple_input(False, 0)
            text = self.visual.TextStim(win=self.win,
                                   text=stimulus.text,
                                   height=text_height,
                                   bold=bold,
                                   colorSpace="rgb",
                                   color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showed: {0}, showing time: {1}", stimulus.text, stimulus.showing_time))
        elif isinstance(stimulus, Sequence_st_text_unit):
            self.event_manager.set_is_activate_one_input(False)
            self.event_manager.set_is_activate_multiple_input(is_multiple_activate = True,
                                                              target_input_count = len(stimulus.texts))
            text = self.visual.TextStim(win=self.win,
                                        text=" - ".join(stimulus.texts),
                                        height=text_height,
                                        bold=bold,
                                        colorSpace="rgb",
                                        color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showed: {0}, showing time: {1}", stimulus.texts, stimulus.showing_time))

    def show_stimuluses(self, stimuluses, text_height=0.3, bold=True, end_message = "", end_process = None):
        stimulus_length = len(stimuluses)

        stimulus = stimuluses[0]
        self.show_stimulus(stimulus, text_height=text_height, bold=bold)

        def show_next_stim():
            # Display manager needs main thread but interface manager occupies main thread when while while loop is running
            # so, display manager gets interface manager to interrupt for displaying stimulus
            self.input_interface_manager.set_interrupt_operation(lambda: self.show_stimuluses(stimuluses[1:]))
            self.input_interface_manager.insert_interrupt(True)

        if stimulus_length > 1:
            if stimulus.showing_time > 0:
                self.show_delay_after(stimulus.showing_time, show_next_stim)
            else:
                show_next_stim()
        else:
            # when stimulus list is over, display manager shows ending message
            def ending():
                self.input_interface_manager.set_interrupt_operation(lambda: self.show_stimulus(Text_st_unit(end_message)))
                if end_process != None:
                    end_process()
                self.input_interface_manager.insert_interrupt(True)
            self.show_delay_after(stimulus.showing_time, ending)

    def show_text_bundle(self, bundle, end_message = "", end_process = None):
        if isinstance(bundle, Text_st_bundle):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_text_bundle(bundle),
                                 end_message=end_message,
                                 end_process=end_process)

    def show_sequence_bundle(self, bundle, end_message = "", end_process = None):
        if isinstance(bundle, Sequence_st_bundle):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_seq_bundle(Sequence_st_bundle),
                                 end_message=end_message,
                                 end_process=end_process)

    def show_package(self, pkg, end_message = "", end_process = None):
        if isinstance(pkg, St_Pakcage):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_pkg(pkg),
                                 end_message=end_message,
                                 end_process=end_process)

    def show_packages(self, pkgs, end_message = "", end_process = None):
        stimuluses = []
        for pkg in pkgs:
            stimuluses += self.make_stimulus_in_pkg(pkg)
        self.show_stimuluses(stimuluses=stimuluses,
                             end_message=end_message,
                             end_process=end_process)

    def make_stimulus_in_text_bundle(self, bundle):
        stimuluses = []
        if isinstance(bundle, Text_st_bundle):
            for j in range(0, len(bundle.units)):
                stimuluses.append(bundle.units[j])
                stimuluses.append(bundle.rumination_units[j])
        return stimuluses

    def make_stimulus_in_seq_bundle(self, bundle):
        stimuluses = []
        for k in range(0, len(bundle.units)):
            stimuluses.append(bundle.units[k])
            stimuluses.append(bundle.rumination_units[k])
        return stimuluses

    def make_stimulus_in_pkg(self, pkg):
        stimuluses = []
        for i in range(0, len(pkg.bundles)):
            bundle = pkg.bundles[i]
            if isinstance(bundle, Text_st_bundle):
                stimuluses += self.make_stimulus_in_text_bundle(bundle)
            elif isinstance(bundle, Sequence_st_bundle):
                stimuluses += self.make_stimulus_in_seq_bundle(bundle)
            stimuluses.append(pkg.interval_units[i])
        return stimuluses

    def close_window(self):
        print("closed window")
        self.win.close()

    def show_delay_after(self, seconds, process):
        t = Timer(seconds, process)
        t.start()

class Input_interface_manager:
    def __init__(self, start_keys, stop_keys, event_manager, device_name="keyboard"):
        self.start_keys = start_keys
        self.stop_keys = stop_keys
        self.device_name = device_name
        self.interrupt_queue = queue.Queue()

        if isinstance(event_manager, Event_manager):
            self.event_manager = event_manager
        else:
            raise Exception("Event_manager Type Error!")

    def set_stop_process(self, stop_proc):
        self.stop_proc = stop_proc

    def wait_start(self):
        if self.device_name == "keyboard":
            while True:
                keys = psychopy.event.getKeys()
                if self.is_inputted_sth(keys):
                    input = self.get_input(keys)
                    print("Input: ", input)
                    if input in self.start_keys:
                        print("Start!")
                        break

    def insert_interrupt(self, is_interrupt):
        self.interrupt_queue.put(is_interrupt)

    def set_device(self, device_name):
        self.device_name = device_name

    def set_interrupt_operation(self, doSomething):
        self.interrupt_operation = doSomething

    def monitoring(self):
        if self.device_name == "keyboard":
            while True:
                if self.interrupt_queue.empty() == False and self.interrupt_queue.get() == True:
                    # if something is interrupted, It processes the thing first
                    # This code is needed because The Keyboard listening is busy-wait so We can't anything while listening is processed
                    if self.interrupt_operation != None:
                        self.interrupt_operation()

                keys = psychopy.event.getKeys()
                if self.is_inputted_sth(keys):
                    input = self.get_input(keys)
                    print("Input: ", input)
                    if input in self.stop_keys:
                        print("Monitoring is Stopped")
                        self.stop_proc()
                        break
                    else:
                        if self.event_manager is not None:
                            self.event_manager.listen_input(input)
                        else:
                            print("Event Manager is not setted out")

    def is_inputted_sth(self, keys):
        return len(keys) != 0

    def get_input(self, keys):
        return keys[0]


class Event_manager:
    def __init__(self, is_activate=True, is_activate_one_input=True, is_activate_multiple_input=True):
        self.is_activate = is_activate
        self.is_activate_one_input = is_activate_one_input
        self.is_activate_multiple_input = is_activate_multiple_input

        self.input_buffer = []

        self.target_input_count = 0

    def listen_input(self, input):
        if self.is_activate == True:
            print("Event Manager is operated: listen_input")
            self.input_buffer.append(input)
            self.listen_one_input(input)
            self.listen_multiple_input(self.input_buffer)

    def listen_one_input(self, input):
        if self.is_activate_one_input == True:
            print("Event Manager is operated: listen_one_input")

    def listen_multiple_input(self, inputs):
        if self.is_activate_multiple_input == True:
            if len(self.input_buffer) == self.target_input_count:
                print("Event Manager is operated: listen_multiple_input")
                self.input_buffer = []
        else:
            self.input_buffer = [] # if not use, clean input buffer

    def set_is_activate(self, is_activate):
        self.is_activate = is_activate
        if is_activate == True:
            print("Event manager is activated")
        else:
            print("Event manager is not activated")

    def set_is_activate_one_input(self, is_one_activate):
        self.is_activate_one_input = is_one_activate
        if is_one_activate == True:
            print("Event manager's is_one_activate is activated")
        else:
            print("Event manager's is_one_activate is not activated")

    def set_is_activate_multiple_input(self, is_multiple_activate, target_input_count):
        self.is_activate_multiple_input = is_multiple_activate
        self.target_input_count = target_input_count
        if is_multiple_activate == True:
            print("Event manager's is_multiple_activate is activated")
        else:
            print("Event manager's is_multiple_activate is not activated")

class Experiment:
    def __init__(self,
                 monitor_size,
                 start_keys = [],
                 stop_keys = [],
                 input_device = "keyboard"):
        """
        Display and interface Setting
        """
        self.event_manager = Event_manager()
        self.interface = Input_interface_manager(start_keys=start_keys,
                                            stop_keys=stop_keys,
                                            event_manager=self.event_manager,
                                            device_name=input_device)

        self.display_manager = Psy_display_manager(self.interface, self.event_manager)
        self.display_manager.open_window(monitor_size, [-1, -1, -1])
        self.interface.set_stop_process(lambda: self.display_manager.close_window())

    def wait_pkg(self, iteration, pkgs, end_message):
        self.display_manager.wait_start(iteration=iteration)

        def start():
            # TODO: CSV 파일 세팅
            self.display_manager.show_packages(pkgs=pkgs,
                                               end_message=end_message)
            self.interface.monitoring()
        start()

    def wait_stimuluses(self, iteration, stimuluses, end_message):
        self.display_manager.wait_start(iteration=iteration)

        def start():
            # TODO: CSV 파일 세팅
            self.display_manager.show_stimuluses(stimuluses=stimuluses,
                                                 end_message=end_message)
            self.interface.monitoring()
        start()

if __name__ == "__main__":
    """
    Basic Usage
    """
    event_manager = Event_manager()
    interface = Input_interface_manager(start_keys=["s"], stop_keys=["q"], event_manager=event_manager,
                                        device_name="keyboard")

    p = Psy_display_manager(interface, event_manager)
    p.open_window([200, 200], [-1, -1, -1])

    p.wait_start(iteration="0")
    p.show_stimuluses([Text_st_unit("1", showing_time=2), Text_st_unit("2", showing_time=3)])

    interface.monitoring()
    p.close_window()

    """
    Experiment Usage
    """