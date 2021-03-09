
import psychopy
from threading import Timer
import queue
from File_Package.sj_file_system import CsvManager
import time

class Direct_fire_timer:
    def start(self, seconds, proc):
        self.proc = proc
        self.timer = Timer(seconds, proc)
        self.timer.start()
    def cancel(self):
        self.timer.cancel()
        self.timer = None
    def direct_proc(self):
        self.cancel()
        self.proc()

class St_Unit:
    def __init__(self, showing_time):
        self.showing_time = showing_time

class Image_st_unit(St_Unit):
    def __init__(self, image_path, showing_time = 0.0):
        super().__init__(showing_time)
        self.image_path = image_path

class Text_st_unit(St_Unit):
    def __init__(self, text, color=[0,0,0], showing_time = 0.0, text_height=0.3):
        super().__init__(showing_time)
        self.text = text
        self.color = color
        self.text_height = text_height

class ISI_st_unit(St_Unit):
    def __init__(self, text, color=[0,0,0], showing_time = 0.0, text_height=0.3):
        super().__init__(showing_time)
        self.text = text
        self.color = color
        self.text_height = text_height

class BundleInterval_st_unit(St_Unit):
    def __init__(self, text, color=[0,0,0], showing_time = 0.0, text_height=0.3):
        super().__init__(showing_time)
        self.text = text
        self.color = color
        self.text_height = text_height

class St_bundle:
    def __init__(self, units):
        self.units = units
        self.ISI_units = []

class Text_st_bundle(St_bundle):
    def __init__(self, units, ISI_times):
        """
        :param units: list of Text_st_unit
        :param ISI_avg_time: average time(Secs) for ISI. if this value is 3 the ISI average time is 3sec per bundle
        """
        # units: list of Text_st_unit
        self.units = units
        self.ISI_times = ISI_times + [0]

        ISIs_stimulus = []
        for i in range(0, len(units)):
            ISIs_stimulus.append(ISI_st_unit("+", showing_time=self.ISI_times[i]))
        self.ISI_units = ISIs_stimulus

class Sequence_st_text_unit(St_Unit):
    #: ex) 3-2-1-4-3
    def __init__(self, text_units, showing_time = 0.0, color = [1,1,1], text_height=0.3):
        self.showing_time = showing_time
        self.color = color
        self.text_height =text_height

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
    def __init__(self, sequences, ISI_interval):
        super().__init__(sequences)
        for i in range(0, len(sequences)):
            self.ISI_units.append(ISI_st_unit("+", showing_time=ISI_interval))

class St_Pakcage:
    def __init__(self, bundles, bundle_intervals, interval_text):
        self.bundles = bundles
        self.bundle_intervals = bundle_intervals

        interval_units = []
        for i in range(0, len(bundles)):
            remain = i % len(bundle_intervals)
            interval_units.append(BundleInterval_st_unit(interval_text, showing_time=bundle_intervals[remain]))
        self.interval_units = interval_units

class Intermediater:
    def __init__(self):
        print("Init Intermeidater")

    def set_input_interface_manager(self, input_interface_manager):
        self.input_interface_manager = input_interface_manager

    def set_display_manager(self, display_manager):
        self.display_manager = display_manager

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager

    def one_input_only(self):
        self.event_manager.set_is_activate_one_input(True)
        self.event_manager.set_is_activate_multiple_input(False, 0)

    def one_multi_input_both(self, multi_input_count):
        self.event_manager.set_is_activate_one_input(True)
        self.event_manager.set_is_activate_multiple_input(is_multiple_activate=True,
                                                          target_input_count=multi_input_count)

    def invalid_event(self):
        self.event_manager.set_is_activate_one_input(False)
        self.event_manager.set_is_activate_multiple_input(False, 0)

    def listen_input(self, input):
        self.event_manager.listen_input(input)

    def set_valid_keys(self, keys):
        self.valid_keys = keys

    def wait_start(self):
        self.input_interface_manager.wait_start()

    def insert_interrupt(self, interrupt):
        self.input_interface_manager.set_interrupt_operation(interrupt)
        self.input_interface_manager.insert_interrupt(True)

class Psy_display_manager:
    def __init__(self, intermediater):
        self.intermediater = intermediater
        self.timer = Direct_fire_timer()
        self.current_step = -1
        self.current_showing_stimlus = None
        self.total_stimuluses = None
        self.stimulus_showing_handler = None

    def open_window(self, size, color = [-1,-1,-1], is_full_screen = False):
        print("open window")
        from psychopy import visual

        self.visual = visual
        self.win = self.visual.Window(size=size,
                                      color=color,
                                      colorSpace='rgb',
                                      fullscr=is_full_screen)

    def set_stimulus_showing_handler(self, handler):
        self.stimulus_showing_handler = handler

    def wait_start(self, ready_keys, stop_keys, iteration):
        # 원래는 interface manager에서 wait key를 하는게 맞으나... 편의상 삽입
        self.show_stimulus(Text_st_unit(""))
        keys = psychopy.event.waitKeys(keyList=ready_keys + stop_keys)

        if keys[0] in ready_keys:
            self.show_stimulus(Text_st_unit(str(iteration) + " trial" + " Ready" ))
            self.intermediater.wait_start()
            return True
        else:
            self.win.close()
            return False

    def show_stimulus(self, stimulus):
        self.current_showing_stimlus = stimulus
        if isinstance(stimulus, Image_st_unit):
            self.intermediater.one_input_only()

            print(str.format("showing stimulus: {0}, showing time: {1}sec", stimulus.image_path, stimulus.showing_time))
            if self.stimulus_showing_handler != None:
                self.stimulus_showing_handler("image", stimulus.image_path, stimulus.showing_time)
        elif isinstance(stimulus, ISI_st_unit):
            text = self.visual.TextStim(win=self.win,
                                        text=stimulus.text,
                                        height=stimulus.text_height,
                                        bold=True,
                                        colorSpace="rgb",
                                        color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showing stimulus: {0}, showing time: {1}sec", stimulus.text, stimulus.showing_time))
            if self.stimulus_showing_handler != None:
                self.stimulus_showing_handler("ISI", stimulus.text, stimulus.showing_time)
        elif isinstance(stimulus, BundleInterval_st_unit):
            self.intermediater.one_input_only()
            text = self.visual.TextStim(win=self.win,
                                        text=stimulus.text,
                                        height=stimulus.text_height,
                                        bold=True,
                                        colorSpace="rgb",
                                        color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showing stimulus: {0}, showing time: {1}sec", stimulus.text, stimulus.showing_time))
            if self.stimulus_showing_handler != None:
                self.stimulus_showing_handler("Bundle Interval", stimulus.text, stimulus.showing_time)
        elif isinstance(stimulus, Text_st_unit):
            self.intermediater.one_input_only()
            text = self.visual.TextStim(win=self.win,
                                   text=stimulus.text,
                                   height=stimulus.text_height,
                                   bold=True,
                                   colorSpace="rgb",
                                   color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showing stimulus: {0}, showing time: {1}sec", stimulus.text, stimulus.showing_time))
            if self.stimulus_showing_handler != None:
                self.stimulus_showing_handler("single text", stimulus.text, stimulus.showing_time)
        elif isinstance(stimulus, Sequence_st_text_unit):
            self.intermediater.one_multi_input_both(len(stimulus.texts))
            text = self.visual.TextStim(win=self.win,
                                        text=" - ".join(stimulus.texts),
                                        height=stimulus.text_height,
                                        bold=True,
                                        colorSpace="rgb",
                                        color=stimulus.color)
            text.draw()
            self.win.flip()
            print(str.format("showing stimulus: {0}, showing time: {1}sec", stimulus.texts, stimulus.showing_time))
            if self.stimulus_showing_handler != None:
                self.stimulus_showing_handler("seq texts", stimulus.texts, stimulus.showing_time)

    def show_stimuluses_with_step_counting(self, stimuluses, end_process = None):
        self.total_stimuluses = stimuluses
        self.show_stimuluses(stimuluses, end_process)

    def show_stimuluses(self, stimuluses, end_process = None):
        # save current step
        stimulus_length = len(stimuluses)
        if self.total_stimuluses != None:
            self.current_step = len(self.total_stimuluses) - stimulus_length

        stimulus = stimuluses[0]
        self.show_stimulus(stimulus)

        def show_next_stim():
            # Display manager needs main thread but interface manager occupies main thread when while while loop is running
            # so, display manager gets interface manager to interrupt for displaying stimulus
            self.intermediater.insert_interrupt(lambda: self.show_stimuluses(stimuluses=stimuluses[1:],
                                                                             end_process=end_process))

        if stimulus_length > 1:
            if stimulus.showing_time > 0:
                self.show_delay_after(stimulus.showing_time, show_next_stim)
            else:
                show_next_stim()
        else:
            # when stimulus list is over, display manager shows ending message
            def ending():
                def last_operation():
                    if end_process != None:
                        end_process()

                self.intermediater.insert_interrupt(last_operation)

            self.show_delay_after(stimulus.showing_time, ending)

    def show_text_bundle(self, bundle, end_process = None):
        if isinstance(bundle, Text_st_bundle):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_text_bundle(bundle),
                                 end_process=end_process)

    def show_sequence_bundle(self, bundle, end_process = None):
        if isinstance(bundle, Sequence_st_bundle):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_seq_bundle(Sequence_st_bundle),
                                 end_process=end_process)

    def show_package(self, pkg, end_process = None):
        if isinstance(pkg, St_Pakcage):
            self.show_stimuluses(stimuluses=self.make_stimulus_in_pkg(pkg),
                                 end_process=end_process)

    def show_packages(self, pkgs, end_process = None):
        stimuluses = []
        for pkg in pkgs:
            if isinstance(pkg, St_Pakcage):
                stimuluses += self.make_stimulus_in_pkg(pkg)
            elif isinstance(pkg, Text_st_unit):
                stimuluses += [pkg]
        self.show_stimuluses(stimuluses=stimuluses,
                             end_process=end_process)

    def show_packages_with_step_counting(self, pkgs, end_process = None):
        stimuluses = []
        for pkg in pkgs:
            if isinstance(pkg, St_Pakcage):
                stimuluses += self.make_stimulus_in_pkg(pkg)
            elif isinstance(pkg, Text_st_unit):
                stimuluses += [pkg]
        self.total_stimuluses = stimuluses
        self.show_stimuluses(stimuluses=stimuluses,
                             end_process=end_process)

    def make_stimulus_in_text_bundle(self, bundle):
        stimuluses = []
        if isinstance(bundle, Text_st_bundle):
            for j in range(0, len(bundle.units)):
                stimuluses.append(bundle.units[j])
                if bundle.ISI_units[j].showing_time > 0:
                    stimuluses.append(bundle.ISI_units[j])
        return stimuluses

    def make_stimulus_in_seq_bundle(self, bundle):
        stimuluses = []
        for k in range(0, len(bundle.units)):
            stimuluses.append(bundle.units[k])
            if bundle.ISI_units[k].showing_time > 0:
                stimuluses.append(bundle.ISI_units[k])
        return stimuluses

    def make_stimulus_in_pkg(self, pkg):
        stimuluses = []
        for i in range(0, len(pkg.bundles)):
            bundle = pkg.bundles[i]
            if isinstance(bundle, Text_st_bundle):
                stimuluses += self.make_stimulus_in_text_bundle(bundle)
            elif isinstance(bundle, Sequence_st_bundle):
                stimuluses += self.make_stimulus_in_seq_bundle(bundle)

            if i != len(pkg.bundles)-1: # 맨 마지막 번들 뒤에는 번들 인터벌 넣어주지 않음
                stimuluses.append(pkg.interval_units[i])
        return stimuluses

    def close_window(self):
        print("closed window")
        self.win.close()

    def show_delay_after(self, seconds, process):
        self.timer.start(seconds, process)

    def show_next_directly(self):
        self.timer.direct_proc()

class Input_interface_manager:
    def __init__(self, start_keys, stop_keys, intermediater, device_name="keyboard"):
        self.start_keys = start_keys
        self.stop_keys = stop_keys
        self.device_name = device_name
        self.interrupt_queue = queue.Queue()
        self.stop_proc = None
        self.is_stop_monitoring = False

        if isinstance(intermediater, Intermediater):
            self.intermediater = intermediater
        else:
            raise Exception("intermediater Type Error!")

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
                    elif input in self.stop_keys:
                        if self.stop_proc != None:
                            self.stop_proc()

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
                        # Interrupt가 일어난 경우에, stop monitoring 콜이 발생한 경우, 루프 중지
                        if self.is_stop_monitoring:
                            self.is_stop_monitoring = False
                            break

                keys = psychopy.event.getKeys()
                if self.is_inputted_sth(keys):
                    input = self.get_input(keys)
                    print("Input: ", input)
                    if input in self.stop_keys:
                        print("Monitoring is Stopped")
                        if self.stop_proc != None:
                            self.stop_proc()
                        break
                    else:
                        if self.intermediater is not None:
                            self.intermediater.listen_input(input)
                        else:
                            print("Event Manager is not setted out")

    def is_inputted_sth(self, keys):
        return len(keys) != 0

    def get_input(self, keys):
        return keys[0]

    def set_is_stop_monitoring(self, is_stop_monitoring):
        self.is_stop_monitoring = is_stop_monitoring

class Event_manager:
    def __init__(self, is_activate=True, is_activate_one_input=False, is_activate_multiple_input=False, valid_keys=None):
        self.is_activate = is_activate
        self.is_activate_one_input = is_activate_one_input
        self.is_activate_multiple_input = is_activate_multiple_input

        self.input_buffer = []

        self.target_input_count = 0
        self.valid_keys = valid_keys

    def listen_input(self, input):
        if self.is_activate == True and (input in self.valid_keys):
            self.input_buffer.append(input)
            self.listen_one_input(input)
            self.listen_multiple_input(self.input_buffer)

    def listen_one_input(self, input):
        if self.is_activate_one_input == True:
            self.single_input_handler(input)

    def listen_multiple_input(self, inputs):
        if self.is_activate_multiple_input == True:
            if len(self.input_buffer) == self.target_input_count:
                self.multiple_input_handler(inputs)
                self.input_buffer = []
        else:
            self.input_buffer = [] # if not use, clean input buffer

    def set_single_input_handler(self, function):
        self.single_input_handler = function

    def set_multiple_input_handler(self, function):
        self.multiple_input_handler = function

    def set_is_activate(self, is_activate):
        self.is_activate = is_activate

    def set_is_activate_one_input(self, is_one_activate):
        self.is_activate_one_input = is_one_activate

    def set_is_activate_multiple_input(self, is_multiple_activate, target_input_count):
        self.input_buffer = []
        self.is_activate_multiple_input = is_multiple_activate
        self.target_input_count = target_input_count

class Experiment:
    def __init__(self,
                 monitor_size,
                 is_full_screen,
                 data_dir_path,
                 participant_name,
                 ready_keys = [],
                 start_keys = [],
                 stop_keys = [],
                 valid_keys = None,
                 input_device = "keyboard"):
        """
        Setting Data
        """
        self.data_dir_path = data_dir_path
        self.participant_name = participant_name
        self.ready_keys = ready_keys

        """
        Display and interface Setting
        """
        self.intermediater = Intermediater()

        self.event_manager = Event_manager(valid_keys=valid_keys)
        self.interface = Input_interface_manager(start_keys=start_keys,
                                                 stop_keys=stop_keys,
                                                 intermediater=self.intermediater,
                                                 device_name=input_device)

        self.display_manager = Psy_display_manager(intermediater=self.intermediater)
        self.display_manager.open_window(size=monitor_size, color=[-1, -1, -1], is_full_screen=is_full_screen)

        self.intermediater.set_input_interface_manager(self.interface)
        self.intermediater.set_display_manager(self.display_manager)
        self.intermediater.set_event_manager(self.event_manager)

        self.start_time = time.time()

        def log_showing(type, stimulus, showing_time):
            # ["Step", "Event_Type", "Stimulus", "display_seconds", "start_seconds"]
            self.stimulus_csv_manager.write_row([self.display_manager.current_step, type, stimulus, showing_time, time.time() - self.start_time])
        self.display_manager.set_stimulus_showing_handler(log_showing)

        self.interface.set_stop_process(lambda: self.display_manager.close_window())

        """
        Setting Events
        """
        def log_response(response):
            # ["Step", "Response", "seconds"]
            self.response_csv_manager.write_row([self.display_manager.current_step, response, time.time() - self.start_time])

        def single_input_handler(input):
            print("proc single input", input)
            log_response(input)

        def multiple_input_handler(inputs):
            print("proc multiple_input", inputs)
            log_response(inputs)

            if isinstance(self.display_manager.current_showing_stimlus, Sequence_st_text_unit):
                self.display_manager.show_next_directly()

        self.event_manager.single_input_handler = single_input_handler
        self.event_manager.multiple_input_handler = multiple_input_handler

    def setting_log(self, iteration):
        self.stimulus_csv_manager = CsvManager(dir_path=self.data_dir_path,
                                               file_name="stimulus_" + self.participant_name + "_" + str(iteration))
        self.stimulus_csv_manager.write_header(
            ["Step", "Event_Type", "Stimulus", "display_seconds", "start_seconds"])
        self.response_csv_manager = CsvManager(dir_path=self.data_dir_path,
                                               file_name="response_" + self.participant_name + "_" + str(iteration))
        self.response_csv_manager.write_header(["Step", "Response", "seconds"])

    def wait_pkg(self, pkgs, iteration, addition_end_proc = None):
        self.setting_log(iteration)

        return_value = self.display_manager.wait_start(iteration=iteration, ready_keys=self.ready_keys, stop_keys=self.interface.stop_keys)

        def start():
            self.start_time = time.time()

            def end_proc():
                self.invalid_input_event()
                if addition_end_proc != None:
                    addition_end_proc()

            self.display_manager.show_packages_with_step_counting(pkgs=pkgs,
                                                                  end_process=end_proc)
            self.interface.monitoring()
        if return_value == True:
            start()

    def wait_blocks(self, blocks, iteration):
        def end():
            if iteration+1 < len(blocks):
                # 기존꺼 멈추고
                self.interface.set_is_stop_monitoring(True)
                # 새로 실행
                self.wait_blocks(blocks, iteration+1)
            else:
                self.display_manager.show_stimulus(Text_st_unit("", showing_time=20))

        self.wait_pkg(pkgs=blocks[iteration], iteration=iteration, addition_end_proc=end)

    def wait_stimuluses(self, stimuluses, iteration, addition_end_proc = None):
        self.setting_log(iteration)

        return_value = self.display_manager.wait_start(iteration=iteration, ready_keys=self.ready_keys, stop_keys=self.interface.stop_keys)

        def start():
            self.start_time = time.time()

            def end_proc():
                self.invalid_input_event()
                if addition_end_proc != None:
                    addition_end_proc()

            self.display_manager.show_stimuluses_with_step_counting(stimuluses=stimuluses,
                                                                    end_process=end_proc)
            self.interface.monitoring()
        if return_value == True:
            start()

    def invalid_input_event(self):
        self.event_manager.set_is_activate_one_input(False)
        self.event_manager.set_is_activate_multiple_input(False, 0)
        print("invalid event_manager")
        self.stimulus_csv_manager.write_row([-1, "End", "End", 0, time.time() - self.start_time])

if __name__ == "__main__":
    """
    Basic Usage
    """
    intermediater = Intermediater()

    event_manager = Event_manager()
    interface = Input_interface_manager(start_keys=["s"], stop_keys=["q"], intermediater=intermediater, device_name="keyboard")
    p = Psy_display_manager(intermediater=intermediater)

    intermediater.set_event_manager(event_manager)
    intermediater.set_input_interface_manager(interface)
    intermediater.set_display_manager(p)

    p.open_window([200, 200], [-1, -1, -1])

    p.show_stimuluses([Text_st_unit("1", showing_time=2), Text_st_unit("2", showing_time=3)])

    interface.monitoring()
    p.close_window()

    """
    Experiment Usage
    """
    source_path = "/Users/yoonseojin/Statistics_sj/CLMN/Replay_Exp"

    data_dir_path = source_path
    participant_name = "seojin"

    exp = Experiment(monitor_size=[400, 400],
                     is_full_screen=False,
                     data_dir_path=data_dir_path,
                     participant_name=participant_name,
                     ready_keys=["r"],
                     start_keys=["s"],
                     stop_keys=["q"],
                     input_device="keyboard")
    exp.wait_stimuluses(stimuluses=[Text_st_unit("ABC", showing_time=1), Text_st_unit("DEF", showing_time=1)],
                        iteration=0)
