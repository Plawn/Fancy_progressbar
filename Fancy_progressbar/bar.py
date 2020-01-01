import time
from .utils import length_of_terminal
from typing import List
from .options import ProgressBarOptions

class ProgressBar():

    _default_animation = ["[|]", "[/]", "[-]", "[\\]"]

    def __init__(self, name: str, *args, fill='█', text='', style='', animation: List[str] = None, options: ProgressBarOptions = None, func=None):

        self.task_name = ""
        self.level = 0
        self._task_name = name
        self.set_taskname()
        self.fill = fill[0]
        self._done = False
        self.hidden = "hidden" in args
        self.textd = text
        self.text_only = len(self.textd) > 0
        self.blankk = "blank" in args
        self.pointer = "pointer" in args   # not supported yet
        self._style = ""  # terminal colors
        self.end_style = ""  # terminal colors
        self._kill_when_finished = "kill_when_finished" in args
        self._current = ''
        self.progress = 0
        self.finished = False
        self._updated = False
        self.event_kill = None
        self.kill_sleep = 0.001
        self._end_style = "\033[m"  # terminal color
        self.current_activated = False
        self.max_length = None

        self.style(style)
        self._animate = True if "animated" in args else False
        self._animation_counter = 0
        
        self._animation = animation if animation is not None else self._default_animation
        self.order = 0  # will be used for the ordered bars
        self.coeff = 1  # to calculate the mean for the family

        # a func and its args to be executed at each refresh
        self.func = func
        self.act_func = True if self.func != None else False

        self.is_child = False
        self.to_suppr = None
        self.final = None

        if options != None:
            self.set_options(options)

    def bind_to(self, obj, final):
        self.pointer = True
        self.progress = obj
        self.final = final

    def __repr__(self):
        return('Bar: {}'.format(self._task_name))

    def set_options(self, options):
        if "hidden" in options.dict["args"]:
            self.hidden = True
        if "blank" in options.dict["args"]:
            self.blankk = True
        if "done" in options.dict["args"]:
            self.done = True
        if "pointer" in options.dict["args"]:
            self.pointer = True
        if "kill_when_finished" in options.dict["args"]:
            self._kill_when_finished = True
        if "animated" in options.dict["args"]:
            self._animate = True

        self.task_name = options.dict["kwargs"].get('taskname', '') + " :"
        self.fill = options.dict["kwargs"].get('fill', '█')[0] if len(
            options.dict["kwargs"].get('fill', '█')) > 0 else '█'
        self.textd = options.dict["kwargs"].get('text', '')
        self.max_length = options.dict["kwargs"].get('max_length', None)
        self._animation = options.dict["kwargs"].get(
            'animation', self._default_animation)
        if len(self.textd) > 0:
            self.text_only = True
        self.style(options.dict["kwargs"].get('style', ''))
        self.current(str(options.dict["kwargs"].get('current', '')))
        # print(self.blankk,self.text_only,self.textd,self._kill_when_finished)

    def name(self, string: str):
        self.task_name = string

    def kill_when_finished(self):
        self._kill_when_finished = True

    def no_style(self):
        self._style = ""
        self.end_style = ""

    def set_child(self):
        self.is_child = True

    def style(self, style):
        if "Style" in str(type(style)):
            self.end_style = self._end_style
            self._style = style.str()
        else:
            if len(style) > 0:
                self.end_style = self._end_style
                self._style = style

    def set_taskname(self):
        self.task_name = '  ' * self.level + self._task_name + ' :'

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def delete(self):
        self._done = True
        self.hidden = True
        self.to_suppr.remove(self)

    def finish(self, **kwargs):
        if self.event_kill != None and self._kill_when_finished:
            self.event_kill.set()
        if not self.current_activated:
            if kwargs.get('showing', False) or kwargs.get('message') != None:
                self._current = str(kwargs.get('message', 'Done'))
                self.current_activated = True
        else:
            self.textd = kwargs.get('message', 'Done')
            self._current = str(kwargs.get('message', 'Done'))
            self.current_activated = True
        self.finished = True
        if self._kill_when_finished:
            time.sleep(0.001)

    def current(self, currentt):
        if isinstance(currentt, str):
            self._current = currentt
            self.current_activated = True
        else:
            raise ValueError("need to be str")

    def done(self):
        self._done = True

    def is_finished(self):
        return self.finished

    def text(self, string):
        self.text_only = True
        self.textd = string

    def blank(self):
        self.text_only = True
        self.blankk = True

    def update(self, progress):
        self.progress = progress
        self._updated = True

    def is_done(self):
        return self._done

    def print_bar(self):
        if self.pointer:
            try:
                progress = self.progress[0]
                if self.final != None:
                    progress = (progress / self.final()) * 100
            except:
                self._done = True
                raise ValueError("can't get value")

        else:
            progress = self.progress
        l = length_of_terminal()

        if self.max_length != None:
            length = l if l < self.max_length else self.max_length
        else:
            length = l
        output = "\r" + self._style
        animation = ""
        if self._animate:
            self._animation_counter += 1
            if self._animation_counter == len(self._animation):
                self._animation_counter = 0
            animation = self._animation[self._animation_counter] + " "

        if not self.text_only:
            dec = str(int(int((progress % 1) * 100)))
            if len(dec) == 1:
                dec += '0'

            t = str(int(progress))  # temp value so no need to re calculate it

            progress_str = t + dec
            length = int(length) - len(self.task_name) - \
                len(progress_str) - len(dec) - 3 - len(animation)

            filledLength = length if progress > 100 else int(
                length * progress / 100)

            bar = self.task_name + animation + self.fill * filledLength + '-' * \
                (length - filledLength) + " " + \
                t + '.' + str(dec) + "%"
            output += bar

            if self.current_activated:
                bottom = self._current + " " * (l - len(self._current))
                if len(bottom) > l:
                    bottom = bottom[0:l - 1] + ">"
                output += "\n" + bottom

        else:
            if not self.blankk:
                if len(self.textd) > length:
                    output += self.textd[0:length - 1] + ">" + self.end_style
                else:
                    output += self.textd + " " * \
                        (length - len(self.textd))
            else:
                return "\r" + " " * length
        output += self.end_style
        return output